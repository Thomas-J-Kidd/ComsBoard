from myLibs import Mqtt
import threading
import time
import paho.mqtt.client as mqtt

stop_thread = False

def on_connect(client, userData, flags, rc):
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(GREEN , "Connected to HIVE MQ", RESET)
    print(YELLOW, "Client is: ", client, RESET)
    print(YELLOW, "Userdata is: ", userData, RESET)
    print(YELLOW, "FLags are: ", flags, RESET)
    print(YELLOW, "Radio Connection: ", rc, RESET)

def on_disconnect(client, userData,  rc):
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(YELLOW, "Client is: ", client, RESET)
    print(YELLOW, "Userdata is: ", userData, RESET)
    print(YELLOW, "Radio Connection: ", rc, RESET)


def on_message(client, userData, message):
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    print(YELLOW, "Client is: ", client, RESET)
    print(YELLOW, "Userdata is: ", userData, RESET)
    print(YELLOW, f"Message: {message.payload.decode()} on topic {message.topic}",RESET)

def start_loop_thread(obj):
    if obj.loop_start():
        print("thread started")

def main():
    global stop_thread
    mqtt_master = Mqtt.MQTTClient(client_id = "Subsite_Master_RPI", on_connect=on_connect, on_disconnect=on_disconnect, on_message=on_message)
    
    # connect to the network 
    mqtt_master.connect()
    
    # sub to topics
    mqtt_master.subscribe("Subsite_Lora_Slave")
    
    # start receive thread
    receive_thread = threading.Thread(target = start_loop_thread, daemon = True)
    
    
    
    if mqtt_master.loop_start():
        time.sleep(0.2)
        while not stop_thread:
            user_input = input("Send Message\tPress 1\nView Publications\tPress 2\nQuit\tPress 3\n")

            if user_input == "1":
                message = input("Enter your message: ")
                if mqtt_master.publish("Subsite_Lora_Master", message):
                    print("message sent")
            elif user_input == "2":
                publications = mqtt_master.get_publications()
                print(publications)
            elif user_input == "3":
                mqtt_master.disconnect()
                mqtt_master.loop_stop()
                stop_thread = True
            
            time.sleep(0.1)

if __name__ == '__main__':
    main()
