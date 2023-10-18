from myLibs import RYLR998
from myLibs import Communications
from myLibs import Buffers
from myLibs import Mqtt
import threading
import time
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
reset = '\033[0m'
blue = '\033[94m'



def radio_setup(callback, settings):
    """
    Sets up the radio object and starts the serial threads

    Args:
    - callback: The callback function that alerts you of a new message
    - settings: The initial port and buffer settings
    
    """
    radio = RYLR998.RYLR998(Communications.SerialDevice, Buffers.CircularBuffer, name="REYAX")
    # print(green + "Object created" + reset)
    
    try:
        radio.open(callback, **settings)
        print(green, "Radio setup successful", reset)
    except Exception as e:
        print(red, "Radio setup unsuccessful",reset)
        print(f"Error: {e}")

    return radio

def callback(message):
    """
    Callback for the serial communication.
    Executes anytime new message is received

    Args: 
    -message(string): The message received via UART

    """

    if message: 
        messageArray = message.split(',')
        message = messageArray[2]
    
        mqtt_send(mqttClient, "RYLR998", message)
        print("Callback: ", message)
    else: 
        return 



settings = {

"RadioConfig":{
    "port":"COM10",
    "baudrate":"115200",
    "timeout":0.1,
    "loopSleep":0.1
},
"Buffer":{
    "bufferSize":100,
    "overflowTimeout": 1,
    "overflowSleep":0.1
    }
}



###########################################################
# MQTT Callbacks
###########################################################


def on_connect_callback(client, userdata, flags, rc):
    """
    Callback for handling the MQTT connect event

    Args:
    - client: the client instace for the callback
    - userdata: the private user data as set in Client() or userdata_set()
    - flags: response flags sent by the broker
    - rc: the connection result
    
    """
    print(green, "MQTT Connected: ", reset)
    # print("Client: ", client)
    # print("Userdata: ", userdata)
    # print("Flags: ", flags)
    # print("RC: ", rc)


def on_disconnect_callback(client, userdata, rc):
    """
        callback for handling the MQTT disconnect event.

        Args: 
        - client: The client instance for this callback.
        - userdata: The private user data as set in Client() or userdata_set().
        - rc: The disconnection result.
        """

    print(red," MQTT Disconnected: ",reset)
    # print("Client: ", client)
    # print("Userdata: ", userdata)
    # print("RC: ", rc)



def on_message_callback(client, userdata, message):
    """
        Handle the message event and perform different funcions
        according to the message

        Args:
        - client: The client instance for this callback.
        - userdata: The private user data as set in Client() or userdata_set().
        - message: An instance of MQTTMessage.
        """
    
    # print(yellow,"On_Message: ",reset)
    # print("Client: ", client)
    # print("Userdata: ", userdata)
    # print(blue, message.payload.decode(), reset)
    dec_message = message.payload.decode()

    if dec_message[0:12] == "AT+PARAMETER":
        mqtt_send(mqttClient, "RYLR998", "Setting new configuration")
        result = radio.commandSendAndValidate(str(dec_message), "+OK")
        return result
    elif dec_message[0:7] == "AT+SEND":
        mqtt_send(mqttClient, "RYLR998", "Sending LoRa message")
        result = radio.sendAndValidate(str(dec_message), "+OK")
        return result
    
    else: 
        return False







###########################################################
# MQTT
###########################################################
def rec_loop_mqtt():
    """
    Starts the receive loop for the MQTT, allowing for continuous MQTT message receival

    Args: 
    none
    
    """
    mqttClient.loop_start()


def start_mqtt_receive(obj, threadName= rec_loop_mqtt,  topic="RYLR998"):
    """
    Subscribes to the topic you want to receive messages from via MQTT
    and starts the thread for continuous MQTT receival

    Args:
    - obj: the MQTT object
    - threadname: the name of the function that initiates the loop for MQTT receiving
    - topic: the topic that you want to subscribe to
    
    """
    try:
        obj.subscribe(topic)
        print(" Subscribed to ", topic)
        receive_thread = threading.Thread(target=threadName, daemon=True)
        receive_thread.start()
        print(green, "MQTT receive threads started", reset)
        

    except Exception as e:
        print("Unable to subscribe to", topic)
        print(f"Error: {e}")

def mqtt_send(obj, topic, message):
    """
    Sends a message to a particular topic via MQTT

    - obj: the MQTT object
    - topic: the topic that you want to publish the message to
    - message: the message that you want to publish
    
    """
        
    try:
        obj.publish(topic, message)
        print(green, f"....Sending Over MQTT: {message}....", reset)

    except Exception as e:
        print("Unable to send message to that topic")
        print(f"Error: {e}")

# Sets up radio object
radio = radio_setup(callback, settings)
# Set up MQTT object
mqttClient = Mqtt.MQTTClient(client_id="REYAX998Device1", on_connect=on_connect_callback, 
                            on_disconnect=on_disconnect_callback, 
                            on_message=on_message_callback, name="RYLR998Device")



mqttClient.connect()

# Start receiving messages via MQTT
start_mqtt_receive(mqttClient, rec_loop_mqtt)

# Initial configuration settings
configuration = {

    "sf":9, 
    "bw": 7, 
    "cr": 4, 
    "pl": 12

}

# Sends configuration to module
radio.configure(configuration)



while True: 
    userIn = input("Enter message")
    
    success = radio.dataSendandValidate(userIn)
    if userIn == 'q' or userIn == 'Q':
        break

    if success: 
        print(green + "Data sent Successfully", reset)
        
    
    
    else:
        print(red + "Data send unsuccessful" + reset)
    success = False





