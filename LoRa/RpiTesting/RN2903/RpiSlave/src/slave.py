from myLibs import Mqtt
import threading
from myLibs import RN2903
from myLibs import Communications
from myLibs import Buffers
import time
import csv
import pandas as pd
import os
import serial.tools.list_ports


# Global variables
global distance

# colors
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
reset = '\033[0m'

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
    global distance
    # print(yellow,"On_Message: ",reset)
    # print("Client: ", client)
    # print("Userdata: ", userdata)
    print(blue,"Incoming message: ", message.payload.decode(), reset)
    # print(blue, message.payload.decode(), reset)
    dec_message = message.payload.decode()
    dec_message = dec_message.split()
    # Saves data to csv if master sends done
    
    
    # If master sends done, save the new data to the csv file
    # and send to master the config line of any configurations that were
    # not received

    if message.payload.decode() == "done":
        add_new_data_to_csv('csv/module_configurations.csv', distance)
        received = check_for_successes('csv/module_configurations.csv')
        mqtt_send(mqttClient, "Subsite_Lora_Slave", str(received))
        print(" Sending received messages over MQTT: ", received)
        received_messages_array = restart_array(received_messages_array)
        


    # Record the distance sent by master for data collection 
    elif dec_message[0] == "distance":
        distance = dec_message[1] 
        print("Testing distance is: ", distance)

    elif dec_message == "save":
        save_to_csv(all_configs_file, "csv/module_configurations.csv")
 
    
    # switch configuration according to what the master sends
    else:
        batch_num = int(message.payload.decode()) 
        print(" Batch number is: ", batch_num)
        new_config = configurations_as_list[batch_num]
        send_config(radio_rn2903,new_config)
        mqtt_send(mqttClient, "Subsite_Lora_Slave", "ok" + str(batch_num))
        # print(new_config)
            

###########################################################
# Radio Callback and functions
###########################################################

def send_config(obj, config_line):
    """
    Send the new configuration to the device

    Args:
    - obj: The radio object that the configuration is for
    - config_line: The new configuration to be sent to the module

    """
    #print("In config: ",config_line)
    if obj.configure(config_line):
        obj._EUI = "0004A30B010C9138"
        obj.stopReceive()
        obj.startReceive()
        return True
    return False


def callback(message):
    """
    Handles new messages from the module

    Args:
    - message: the message that is received from the module

    """
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    radio_rn2903.commandSendAndReceive("radio rx 0")
    #print(result)
    result = message.split()
    # print(result[0])
    
    # Handles if the module returns radio_err
    if result[0] == "radio_err":
       print(RED, "radio error occured", RESET)

       # Marks the config line as passed and prints the configline
       # to the terminal
    else:    
        id = bytes.fromhex(result[1][:32]).decode()
        packages = int.from_bytes(bytes.fromhex(result[1][32:36]), 'big')
        dash = bytes.fromhex(result[1][36:38]).decode()
        currentPackage = int.from_bytes(bytes.fromhex(result[1][38:42]), 'big')
        data = bytes.fromhex(result[1][42:])
        config_line = int(data)
        
        # Send verification over MQTT
        mqtt_send(mqttClient, "Subsite_Lora_Config_Status", f"Config line {config_line} received")
        # storing data 
        received_messages_array[config_line] = 1
        # print(received_messages_array)

        print(YELLOW, f"Config Line: {config_line}", RESET)
            #print(f"RECEIVED-> ID: {id} Package: {packages}{dash}{currentPackage} data: {data}")
        
                
    
def save_to_csv(df, file):
    """
    Saves a pandas dataframe to a .csv file

    Args:
    - df: the pandas dataframe that you want to save
    - file: the filename you want to save the dataframe to
    
    """
    df.to_csv(file, index=False)


# Adds the new column of data to the .csv file           
def add_new_data_to_csv(file,distance):
    """
    Adds the pass/fail data to the .csv file with the name
    of the column being the distance that was decided by the master

    Args:
    - file: the filename that you want to save the new data to
    - distance: the distance or name you want the column to have
    
    """
    df = pd.read_csv(file)
    df[distance] = received_messages_array
    save_to_csv(df,file)

def restart_array(array):
    for item in array:
        item = 0
    return array


# Creates a new array of all configs that failed
def check_for_successes(file):
    """
    Iterates through the collected data and returns an array 
    of all configuration lines that were successful

    Args:
    - file: The .csv file that we are checking for successful transmissions in
    
    """
    received = []
    with open(file, 'r') as file:
        configs = csv.reader(file)
        distance_index = len(next(configs))-1
        print("CSV last column index: ", distance_index)

        counter = 0
        for row in configs: 
            if row[distance_index] == '1':
                received.append(counter)
            counter += 1
    return received


###########################################################
# Sets up the radio
# Starts send/receive threads
###########################################################


def find_os():
    """
    Args:
        - None

    Purpose:
        - detects the operating system you are using (currently windows, linux, and mac)
        - lets you choose the serial COM port based on your operating system
        - returns the port you are wanting to use
        
    
    Future additions:
        - automate the port detection to eliminate user input error
        - add other operating systems besides windows, mac, and linux
        - only been tested on linux and windows
    """
    os_name = os.name
    if os_name == "posix":
        print("Running on a Unix-like system (e.g., Linux, macOS)")

        # Get a list of all available serial ports
        ports = serial.tools.list_ports.comports()

        # Iterate over the ports and print information about each port
        for port in ports:
            print(f"Device: {port.device}, Description: {port.description}")
        
        choosen_port=input("choose from the list of ports availble: ")
        return choosen_port

    elif os_name == "nt":
        com_ports = list(serial.tools.list_ports.comports())
        for port in com_ports:
            print(f"Serial ports found: {port.device}, Description: {port.description}")
        choosen_port=input("choose from the list of ports availble: ")
        return choosen_port
        
    elif os_name == "java":
        print("Running on Java Virtual Machine")

    else:
        print("Unknown operating system")



def radio_setup(callback, settings):
    """
    Sets up the radio object and starts the serial threads

    Args:
    - callback: The callback function that alerts you of a new message
    - settings: The initial port and buffer settings
    
    """
    radio = RN2903.RN2903_Radio(Communications.SerialDevice, Buffers.CircularBuffer, name="SLAVE")
    # print(green + "Object created" + reset)
    
    try:
        radio.open(callback, **settings)
        print(green, "Radio setup successful", reset)
    except Exception as e:
        print(red, "Radio setup unsuccessful",reset)
        print(f"Error: {e}")

    return radio

    
    

    

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


def start_mqtt_receive(obj, threadName= rec_loop_mqtt,  topic="Subsite_Lora_Master"):
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

port = find_os()


settings = {

"RadioConfig":{
    "port":port,
    "baudrate":"57600",
    "timeout":0.1,
    "loopSleep":0.1
},
"Buffer":{
    "bufferSize":100,
    "overflowTimeout": 1,
    "overflowSleep":0.1
    }
}
    

# Sets up radio
radio_rn2903 = radio_setup(callback, settings)

# Set up MQTT object
mqttClient = Mqtt.MQTTClient(client_id="SubsiteSlave1234", on_connect=on_connect_callback, 
                            on_disconnect=on_disconnect_callback, 
                            on_message=on_message_callback, name="Slave")
# connect to MQTT Broker
mqttClient.connect()
print(green, "MQTT connected",reset)

# Start receiving messages via MQTT
start_mqtt_receive(mqttClient, rec_loop_mqtt)



# File that contains all 73 batch configuration for slave
batch_config_file = 'csv/module_configurations_slave.csv'

# File that contains all 1225 configurations that master will test
# Slave will edit this file according to whether that configuration worked
all_configs_file = 'csv/module_configurations.csv'

# Converts .csv file of configurations to pyton array to allow 
# access to certain indices
with open(batch_config_file, "r") as file:
        configurations = csv.DictReader(file)
        configurations_as_list = []

        for row_dict in configurations:
            row_dict["bw"] = int(row_dict["bw"])
            configurations_as_list.append(row_dict)


# create array to store data
with open(all_configs_file, "r") as all_configs_file:
    received_messages_array = []
    for line in all_configs_file:
            received_messages_array.append(0)
    received_messages_array.pop()


# simply just keeps the program running
# The sleep just keeps this from printing ontop of threads
while True: 
    time.sleep(0.5)
    userIn = input(" Type q to quit and save")

    if userIn == 'q':
        add_new_data_to_csv('csv/module_configurations.csv', distance)
        break
    # print("Waiting for batch number", end="\r")
    















