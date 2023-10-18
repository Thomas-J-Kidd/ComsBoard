### Overview

This is a repository for testing the RYLR998 LoRa module's range using P2P. As the file names suggest, one file is specifically for the receiver and the other is the transmitter. Both files have a simple CLI that allows you to communicate between the modules by typing your message. For testing, we used two Raspberry Pi 3 Model B+'s. We then used MQTT to send messages, and change configurations. This process is outlined below. With MQTT we were able to use our phones and manually send a message to the pi via MQTT, then the Pi would forward that message via LoRa to the other module. We were also able to change the configuration setting via MQTT as well. This setup allowed us to be more mobile and provide a longer battery life when testing, using our phones to monitor the code via MQTT. 

### Usage Instructions

1. Download MyMQTT app on your smartphone
   
2. Subscribe to the topic **RYLR998**. This is the topic that you will send your configurations and messages to.
   
3. Run the code on the desired Pi/computer. If using a raspberry Pi make sure it is connected to the internet or a hotspot, or the MQTT will not work. 
   
4. To tell the **RYLR998_sender.py** to send a message, send this AT command over MQTT to the **RYLR998** topic.
   ```AT+SEND=<Address>,<Payload Length>,<Data>```
   The address is default 0, which is what it is also set to in the code.
   When the sender sends a message it will send "Sending LoRa message"
   Example use:
   ```AT+SEND=0,5,hello```
   If the receiver module receives the message, it will respond with "LoRa message recieved: hello" over MQTT. Where hello is whatever message you choose to send to the module.

5. To set both modules to a new configuration, send the following command over MQTT:
   ```AT+PARAMETER=<Spreading Factor>,<Bandwidth>,<Coding Rate>,<Programmed Preamble>```
        Example use:
        ```AT+PARAMETER=9,7,1,12```
        This will automatically update the configurations of both modules. 
   - Spreading factor values: 5-11
   - Bandwidth values: 7-9
     - 7: 125KHz, only usable with spreadfactors 7-9
     - 8: 250KHz, only usable wiht spreadfactors 7-10
     - 9: 500KHz, only usable with spreeadfactors 7-11
   - Coding Rate Values: 1-4
   - Preamble values: Must be 12, unless NETWORKID=18. In this case it may be 4-24.