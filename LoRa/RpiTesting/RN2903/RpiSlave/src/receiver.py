##### slave LoRa RPI #####

# imports
from myLibs import RN2903
from myLibs import Communications
from myLibs import Buffers
import pandas as pd
from datetime import datetime
import math
import time
import csv
import os
import glob

# objects
def create_obj():
    radio = RN2903.RN2903_Radio(Communications.SerialDevice, Buffers.CircularBuffer, name="SLAVE")
    return radio


########################################################
#           configuration commands                     #
########################################################


def read_config(file):
    try:
        df = pd.read_csv(file, header=0)
    except FileNotFoundError:
        print("Config file not found. Please check the file path.")
    except pd.errors.ParserError:
        print("Error occurred while parsing the CSV file.")
    return df


def read_batch(file): 
    try:
        df = pd.read_csv(file, header=0)
    except FileNotFoundError:
        print("Batch file not found. Please check the file path." )
    except pd.errors.ParserError:
        print("Error occurred while parsing the CSV file.")
    return df

def get_config(index, config):
    configRow = config.iloc[index]
    configRowAsKwargs = configRow.to_dict()
    return configRowAsKwargs

def save_to_csv(df, file):
    df.to_csv(file, index=False)

def find_os():
    os_name = os.name
    if os_name == "posix":
        print("Running on a Unix-like system (e.g., Linux, macOS)")
        serial_ports = glob.glob('/dev/tty[A-Za-z]*')

    # Iterate over the list of serial ports
        for port in serial_ports:
            print(f"Serial Port found: {port}")
            if port == "/dev/ttyUSB0":
                return port
        return "port not found"
    elif os_name == "nt":
        com_ports = list(serial.tools.list_ports.comports())
        for port in com_ports:
            print(f"Serial ports found: {port.device}, Description: {port.description}")
        return port.device
    elif os_name == "java":
        print("Running on Java Virtual Machine")
    else:
        print("Unknown operating system")


def save_new_data_to_csv(file):
    df = pd.read_csv(file)
    df['pass/fail'] = received_messages_array
    save_to_csv(df,file)




########################################################
#                   radio commands                     #
########################################################


# radio setup
def radio_setup(obj, callback, settings):
    # sets up the radio to send and receive messages
    obj.open(callback, **settings)
    return True



# send configurations to device
def send_config(obj, config_line):
    #print("In config: ",config_line)
    if obj.configure(config_line):
        obj._EUI = "0004A30B010C9138"
        obj.stopReceive()
        obj.startReceive()
        return True
    return False

# Callback function
def callback(message):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    radio_rn2903.commandSendAndReceive("radio rx 0")
    #print(result)
    result = message.split()
    # print(result[0])
    

        

    if result[0] == "radio_err":
       print(RED, "radio error occured", RESET)
    else:    
        id = bytes.fromhex(result[1][:32]).decode()
        packages = int.from_bytes(bytes.fromhex(result[1][32:36]), 'big')
        dash = bytes.fromhex(result[1][36:38]).decode()
        currentPackage = int.from_bytes(bytes.fromhex(result[1][38:42]), 'big')
        data = bytes.fromhex(result[1][42:])
        line = int(data)

        # storing data 
        received_messages_array[line] = 1
        # print(received_messages_array)

        print(YELLOW, f"Config Line Number: {line}", RESET)
            #print(f"RECEIVED-> ID: {id} Package: {packages}{dash}{currentPackage} data: {data}")


########################################################
#                 syncing commands                     #
########################################################

# function to sync up to the nearest minute
def sync_to_start():
    
    # get the current time
    current_time = datetime.now()
    print('Current time: ', current_time)
    to_time = 60 #sync on the minute
    seconds_remaining = to_time - current_time.second
    print('Seconds remaning until the first batch is sent: ', seconds_remaining)
    print('...syncing...') 
    # Sleep until the next leading minute
    time.sleep(seconds_remaining)
    return True


def sync_to_next_batch(next_batch_number, batch_time):
    # read the time on air from the current next batch number
    # **for testing purposes we are making the default time on air 15 seconds**
    current_time = datetime.now()
    print("Syncing to next batch")
    #print("Current time: ", datetime.now())
    
    while True:
        current_time = datetime.now()
        if current_time.second % 60 == 0:
            process_start_time  = datetime.now()
            waited_time = process_start_time.second-current_time.second
            print("Process started at time: ", process_start_time)  
            print("Time spent syncing: ", waited_time)
            print("Air time: ", batch_time)
            return True



# TODO possibly delete main/add global variables

# def main():
   
# variables
batch_config_file = 'csv/module_configurations_slave.csv'
batch_time_file = 'csv/batch_file.csv'
all_configs_file = 'csv/module_configurations.csv'


# colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
# port = find_os()
#port = input("Enter port: ")
settings = {

"RadioConfig":{
    "port":"COM4",
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

# creating the object
radio_rn2903 = create_obj()

print(GREEN + "Object created" + RESET)

# radio setup
if radio_setup(radio_rn2903, callback, settings):
    print(GREEN + "radio setup successful" + RESET)
else:
    print(RED + "radio setup failed"+ RESET)

# syncing
current_time = datetime.now().second


# create array to store data
with open(all_configs_file, "r") as all_configs_file:
    received_messages_array = []
    for line in all_configs_file:
            received_messages_array.append(0)
    received_messages_array.pop()



while current_time != 0:
    start_time = 60 - current_time
    print(f"Starting in: {start_time} ", end="\r")
    time.sleep(1)
    current_time = datetime.now().second

print(GREEN + "Started" + RESET)

with open(batch_config_file, "r") as file:
    configurations = csv.DictReader(file)
    config_counter = 0
    for row_dict in configurations:
        #print(YELLOW, row_dict['sf'], row_dict['cr'], row_dict['pwr'], RESET)
        row_dict["bw"] = int(row_dict["bw"])
        print(row_dict)
        if send_config(radio_rn2903, row_dict):
            current_time = datetime.now().second
            print(GREEN, "Receiving batch: ",config_counter, RESET)
            config_counter += 1
            while current_time != 0 and current_time != 30:
                start_time = 60 - current_time
                #print(f"Next config in: {start_time}\r")
                time.sleep(.1)
                current_time = datetime.now().second
                # print(current_time)
            time.sleep(.7)


    save_new_data_to_csv('csv/module_configurations.csv')
    

           


# if __name__ == "__main__":
#     main()
