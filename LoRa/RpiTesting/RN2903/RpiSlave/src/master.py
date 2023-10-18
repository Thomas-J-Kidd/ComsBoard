#### master LoRa RPI #####
"""@package docstring
Documentation for this module.
 
More details.
"""
# imports
import csv
from datetime import datetime
import math
import time
import os
import serial.tools.list_ports
import glob
import threading
import paho.mqtt.client as mqtt
import re

# Subsite Libraries
from myLibs import Mqtt
from myLibs import RN2903
from myLibs import Communications
from myLibs import Buffers
#from myLibs import Mqtt

# variables
stop_program = False
mqtt_message = ""
mqtt_topic = ""

# objects
def create_obj():
    """ 
    Args:
        - None

    Purpose:
        - Creates he RN2903 object required for using the LoRa device
        - returns the radio object
        - sets the EUI for the LoRa Module as well

    Future additions:
        - be able to use other LoRa Module devices
    """

    radio = RN2903.RN2903_Radio(Communications.SerialDevice, Buffers.CircularBuffer, name="MASTER")
    radio._EUI = "0004A30B010C9138"

    return radio

########################################################
#           configuration commands                     #
########################################################
# send configurations to device
def send_config(obj, config_line):
    
    """
    Args: 
        - obj
            * type: object
            * purpose: be able to use the RN2903 object
        - config_line
            * type: dict
            * prupose: containts the different LoRa configurations
    
    Purpose:
        - sends the configurations to the device
        - returns True or False if successfull or not
    """

    if obj.configure(config_line):
        return True
    return False

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


########################################################
#                   radio commands                     #
########################################################



# radio setup
def radio_setup(obj, callback, settings):
    """
    Args:
        - obj
            * type: object
            * purpose: is the LoRa Module object
        
        - callback
            * type: function
            * purpose: function that prints out received information over LoRa

        - settings:
            * type: nested dictionary (2 layers)dd
            * purpose: containt the Communications and Buffer classes settings


    Purpose:
        - opens the port and starts the threads in the Communications.py class
    """
    obj.open(callback, **settings)
    return True

def send_data(obj, config, config_line):
    """
    Args:
        - obj
            * type: obj
            * purpose: is the Lora Module object
        - config
            * type: dict
            * purpose: is the configuration to be sent to the module
        - config line
            * type: int
            * purpose: is the data that we are sending over LoRa

    Purpose:
        - loads a specified configuration to the LoRa Module
        - sends a message using that configuration. In this specific example it is sending the line number of our test file

    """
    send_config(obj, config)
    data = f"{config_line}"
    if obj.stopReceive():
        if obj.dataSend(data):
            return True
        return False

def callback(message):
    """
    Args:
        - message
            * type: hex
            * purpose: containts the infomration from the received LoRa message
    Purpose:
        - decodes the custom header built by Carlos
        - outputs the information received to the terminal 
    """

    #print(f"CALLBACK 1: {message}")
    result = message.split()
    id = bytes.fromhex(result[1][:32]).decode()
    packages = int.from_bytes(bytes.fromhex(result[1][32:36]), 'big')
    dash = bytes.fromhex(result[1][36:38]).decode()
    currentPackage = int.from_bytes(bytes.fromhex(result[1][38:42]), 'big')
    data = bytes.fromhex(result[1][42:])
    incomingMessage = str(data)
    print(f"RECEIVED-> ID: {id} Package: {packages}{dash}{currentPackage} data: {data}")
    


########################################################
#                 syncing commands                     #
########################################################

def input_thread():
    """
    Args:
        - None
    Purpose:
        - stops the program when the user presses a key on the screen

    """
    global stop_program
    # Poll for user input
    while not stop_program:
        if input("press any key to quit: "):  # Check if 'q' key is pressed
            stop_program = True

########################################################
#                    MQTT commands                     #
########################################################

def on_connect(client, userData, flags, rc):

    """
    Args:
        - client
            * type: class 'paho.mqtt.client.Client'
            * purpose: contains information about the mqtt client in our program
        - userData
            * type: class 'NoneType', can be any type
            * purpose: user data paramet passed to the callbacks
        - Flags
            * type: class 'dict'
            * purpose: response flags sent by the broker
        - rc
            * type: class 'int'
            * purpose: the connection result, 
                0: Connection successful 
                1: Connection refused - incorrect protocol version 
                2: Connection refused - invalid client identifier 
                3: Connection refused - server unavailable 
                4: Connection refused - bad username or password 
                5: Connection refused - not authorised 
                6-255: Currently unused.
    Purpose:
        - Callback to the on_connect function within the PAHO mqtt class
        - prints out the client details upon connecting to the mqtt broker
    """

    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(GREEN , "Connected to HIVE MQ", RESET)
    print(YELLOW, "Client is: ", client,RESET)
    print(YELLOW, "Userdata is: ", userData,  RESET)
    print(YELLOW, "Flags are: ", flags, RESET)
    print(YELLOW, "Radio Connection: ", rc, RESET)

def on_disconnect(client, userData,  rc):
    """
    Args:
        - client
            * type: class 'paho.mqtt.client.Client'
            * purpose: contains information about the mqtt client in our program
        - userData
            * type: class 'NoneType', can be any type
            * purpose: user data paramet passed to the callbacks
        - rc
            * type: class 'int'
            * purpose: the connection result, 
                0: disconnection was successful
                1-255: unexpected disconnect
    Purpose:
        - Callback to the on_disconnect function in the PAHO mqtt class
        - prints information when the client disconnects from the mqtt broker
    """

    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(YELLOW, "Client is: ", client, RESET)
    print(YELLOW, "Userdata is: ", userData, RESET)
    print(YELLOW, "Radio Connection: ", rc, RESET)


def on_message(client, userData, message):
    """
    Args:
        - client
            * type: class 'paho.mqtt.client.Client'
            * purpose: contains information about the mqtt client in our program
        - userData
            * type: class 'NoneType', can be any type
            * purpose: user data paramet passed to the callbacks
        - message
            * type: class 'paho.mqtt.client.MQTTMessage'
            * purpose: the incoming message through mqtt
            * usage: use message.payload.decode() to decode the message to a str 

    Purpose:
        - displays the message
        - returns mqtt_message as a global variable for the rest of the program to access

    """
    global mqtt_message
    mqtt_message = check_message(message.payload.decode(), message.topic)
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(YELLOW, "Client is: ", client, RESET)
    print(YELLOW, "Userdata is: ", userData, RESET)
    print(YELLOW, f"Message: {message.payload.decode()} on topic {message.topic}",RESET, type(message))

def start_loop_thread(obj):
    """
    Args:
        - obj
            * type: object
            * purpose: able to access the functions in the mqtt class

    Purpose:
        - starts the loop for the MQTT class
    """
    if obj.loop_start():
        print("thread started")

def check_message(message, topic):
    """
    Args:
        - message
            * type: str
            * purpose: containts the information we pass in message
        - topic
            * type: str
            * purpose: containts the information we pass in topic
    Purpose:
        - we use this function in the message callback to determine what topic we received the message from
        - different settings are encoded depending on the topic
    """

    if message == "auto" and topic == "Subsite_Lora_Master_Phone":
        return "auto"
    if message == "all" and topic == "Subsite_Lora_Master_Phone":
            return "all"
    elif message == "manual" and topic == "Subsite_Lora_Master_Phone":
        return "manual"
    elif message == "stop" and topic == "Subsite_Lora_Master_Phone":
        return "stop"
    elif message == "reset" and topic == "Subsite_Lora_Master_Phone":
        return "reset"
    elif message[0:5] == "batch" and topic == "Subsite_Lora_Master_Phone":
        return message 
    elif message[0:4] == "line" and topic == "Subsite_Lora_Master_Phone":
        return message 
    else:
        return message

def test_all_configurations(test_file, mqtt_master, radio_rn2903):
    """
    Args:
        - test_file
            * type: string 
            * purpose: embeds the csv file
        - mqtt_master
            * type: object
            * purpose: allows for the usage of the Mqtt class
        - radio_rn2903
            * type: object
            * purpose: allows for the usage of the RN2903_Radio class
    Purpose:
        - Tests all the configurations possible
        - Use MQTT conformation to send new batches
    """

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    global mqtt_message
    batch_num = -1
    config_counter = 0
    conformation=""

    print("in all")
    with open(test_file, "r") as file:
        configurations = csv.DictReader(file)
        for row_dict in configurations:
            if batch_num != int(row_dict["batch_num"]):
                batch_num = int(row_dict["batch_num"])
                mqtt_master.publish("Subsite_Lora_Master", int(row_dict["batch_num"]))
                print(GREEN, f"Sent batch {batch_num} over MQTT, waiting on response", RESET)
                conformation = "ok"+str(batch_num)
                while (mqtt_message != conformation):
                    time.sleep(0.1)
            #if mqtt_message == conformation: 
            row_dict["bw"] = int(row_dict["bw"])
            if send_data(radio_rn2903, row_dict, configurations.line_num-1):
                print(GREEN, configurations.line_num-1, RESET)

            if mqtt_message == "reset":
                return False
        return True

def test_race_horse(test_file, mqtt_master, radio_rn2903):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
   
    global mqtt_message
    batch_num = -1
    config_counter = 0
    conformation=""

    with open(test_file, "r") as file:
        configurations = csv.DictReader(file)
  
        for row_dict in configurations:
            if batch_num != int(row_dict["batch_num"]):
                batch_num = int(row_dict["batch_num"])
                if batch_num < 72:
                    mqtt_master.publish("Subsite_Lora_Master", batch_num)
                    print(GREEN, f"Sent batch {batch_num} over MQTT, waiting on response", RESET)
                    conformation = "ok"+str(batch_num)
                    while (mqtt_message != conformation):
                        time.sleep(0.1)
                    if mqtt_message == conformation: 
                        row_dict["bw"] = int(row_dict["bw"])
                        if send_data(radio_rn2903, row_dict, (configurations.line_num-2)):
                            print(GREEN, configurations.line_num-2, RESET)
                            time.sleep(0.1)

                    if mqtt_message == "reset":
                        break;
                            
        mqtt_master.publish("Subsite_Lora_Master", "distance 1234")        
        mqtt_master.publish("Subsite_Lora_Master", "done")


        time.sleep(2)
        print(mqtt_message)
        configurations = re.findall(r"\d+", mqtt_message)
        configurations = list(map(int, configurations))
        counter = 0
        for received in configurations:
            print("Counter: ", counter) 
            batch_num = int((configurations[counter])/18)
            print("Line received: ", received)
            print("Batch is: ", batch_num)

            mqtt_master.publish("Subsite_Lora_Master", batch_num)
            print(GREEN, f"Sent batch {batch_num} over MQTT, waiting on response", RESET)
            conformation = "ok"+str(batch_num)
            while (mqtt_message != conformation):
                time.sleep(0.1)
            if mqtt_message == conformation: 

                for i in range(17):
                    row_dict = get_line_as_dict(test_file, received+i+2)
                    row_dict['bw'] = int(row_dict['bw'])
                    send_data(radio_rn2903, row_dict, batch_num*17+i)
                                           
            counter += 1
        return True

def test_manual(test_file, mqtt_master, radio_rn2903):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    global mqtt_message
    batch_num = -1
    config_counter = 0
    conformation=""
    mqtt_sent = False

    with open(test_file, "r") as file:
        configurations = csv.DictReader(file)

        if mqtt_message=="manual":
            while not mqtt_sent:            
                if mqtt_message[0:4] == "line" and not mqtt_sent: 
                    line_num = mqtt_message[4:]
                    mqtt_master.publish("Subsite_Lora_Master", line_num)
                    print(GREEN, f"Sent line number {line_num} over MQTT, waiting on response", RESET)
                    conformation = "ok"+str(line_num)
                    mqtt_message = ""
                if mqtt_message == conformation:
                    line_num = int(line_num)
                    row_dict = get_line_as_dict(test_file, line_num)
                    row_dict["bw"] = int(row_dict["bw"])
                    send_data(radio_rn2903, row_dict, line_num)
                    mqtt_message = ""
                    mqtt_sent=True

                if mqtt_message == "reset":
                    return False
        return True

def get_line_as_dict(csv_file, line_number):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)

    # Check if the line number is within the range of lines in the file
    if line_number < 1 or line_number > len(lines):
        return None  # Invalid line number

    # Get the line at the specified line number
    line = lines[line_number - 1]

    # Convert the line into a dictionary
    header = lines[0]  # Assuming the first line is the header
    line_dict = {header[i]: line[i] for i in range(len(header))}

    return line_dict

def run(mqtt_master, radio_rn2903, test_file):

    """
    Args:
        - mqtt_master
            * type: object
            * purpose: gives us access to the mqtt class
        - radio_rn2903,
            * type: object
            * purpose: gives access to the Radio RN2903 class
        - test_file
            * type: str
            * purpose: containts the information for the location of the test file. CSV format

    Purpose:
        - opens the csv file
        - has 5 modes
            * mode all: tests all the possible configurations
            * mode test: tests the 72 batch configurations (this is to be updated to make the race horse algorithim faster)
            * mode manual: specify a batch number or config number to your liking
            * mode reset: restarts the menu and you can executre all, test, or manual
            * mode stop: stops the run function and exits
    """

    # local variables
    stop_thread=False
    mqtt_sent=False
    conformation=""
    batch_num = -1

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    # global variables
    global stop_program
    global mqtt_message # from callback
    
    print("\nwaiting for directions",end = "\r")
    while not stop_thread:
        if mqtt_master.loop_start():
            time.sleep(0.2)
            if mqtt_message == "all":
                print(GREEN, "starting all", RESET, end = "\r")
                if test_all_configurations(test_file, mqtt_master, radio_rn2903):
                    print(GREEN, "\nDone testing all configurations", RESET)
                    mqtt_master.publish("Subsite_Lora_Master", "distance 1")
                    mqtt_master.publish("Subsite_Lora_Master", "done")

            elif mqtt_message == "race horse":
                print(GREEN, "\nstarting race horse", RESET)
                if test_race_horse(test_file, mqtt_master, radio_rn2903):
                    print("\nDone testing race horse", RESET)
                    mqtt_master.publish("Subsite_Lora_Master", "distance 1")
                    mqtt_master.publish("Subsite_Lora_Master", "done")

            elif mqtt_message == "manual":
                print(GREEN, "\nstarting manual mode", RESET)
                if test_manual(test_file, mqtt_master, radio_rn2903):
                    print(GREEN, "\nDone testing in manual mode", RESET)
                    mqtt_master.publish("Subsite_Lora_Master", "distance 1")
                    mqtt_master.publish("Subsite_Lora_Master", "done")

            elif mqtt_message=="stop":
                 stop_thread = True


def main():
   
    # variables
    port = find_os()
    #port="/dev/ttyUSB0"
    stop_thread=False
    mqtt_sent=False

    # files
    test_file = "csv/csv_test_with_batch_label.csv"

    # colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
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


    # mqtt object
    mqtt_master = Mqtt.MQTTClient(client_id = "Subsite_Master_RPI", on_connect=on_connect, on_disconnect=on_disconnect, on_message=on_message)
    
    # connect to the network 
    mqtt_master.connect()
    
    # sub to topics
    mqtt_master.subscribe("Subsite_Lora_Slave")
    mqtt_master.subscribe("Subsite_Lora_Master_Phone")
    
    # start receive thread for mqtt
    receive_thread = threading.Thread(target = start_loop_thread, daemon = True)
        
    # creating the object
    radio_rn2903 = create_obj()
    print(GREEN + "Object created" + RESET)

    # radio setup
    if radio_setup(radio_rn2903, callback, settings):
        print(GREEN + "radio setup successful" + RESET)
    else:
        print(RED + "radio setup failed"+ RESET)

    # start the test function
    run(mqtt_master,radio_rn2903, test_file)
    


    #TODO save csv
if __name__ == "__main__":
    main()
