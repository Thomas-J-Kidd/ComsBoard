:py:mod:`master`
================

.. py:module:: master

.. autoapi-nested-parse::

   This program, master.py, is one of the Raspberry Pi 3b+ that helped test the LoRa module, RN2903s range. 

   **Before running any tests**
   ===========================================================================
   1) Reset the csv files on the slave device
   2) make sure your RPI is configured to connect to your phones hotspot (guide can be found on the html website)


   **Program flow**
   ===========================================================================
   1) The master program connects to the MQTT client  
   2) Subcribe to topics
   3) Create Rn2903 objects and set up callbacks
   4) Execute run() function to go into main menu
   5) Choose between 4 modes:
       - all (tests all the configs)
       - race horse (tests only certain batches. Tests the 12th spreadfactor by default)
       - manual (tests only the specific line number )
       - exit (goes back to main menu)

   **Description of each mode**
   ===========================================================================
   **all**
   ---------------------------------------------------------------------------
   1) send "**all**" to the topic "**Subsite_Lora_Master_Phone**"
   2) send "**distance (number)**" to the topic "**Subsite_Lora_Master_Phone**". This will allow the slave device to save a column of the csv file with the specific distances received from the test. The number can refer to the current test number you are running. **You must pass a number!**

   This will start a ping pong reaction of testing all of the configurations possible. The estimated time this takes is about 30 minutes. 

   **race horse**
   ---------------------------------------------------------------------------
   1) send "**race horse**" to the topic "**Subsite_Lora_Master_Phone**"
   2) send "**distance (number)**" to the topic "**Subsite_Lora_Master_Phone**". This will allow the slave device to save a column of the csv file with the specific distances received from the test. The number can refer to the current test number you are running. **You must pass a number!**

   This will start the race horse methodology which tests only specific batches. The default batches are from 59 to 72 as these are the sf12 bathces. (longest range)

   **manual**
   ---------------------------------------------------------------------------
   1) send "**manual**" to the topic "**Subsite_Lora_Master_Phone**". 
   2) send "**line(number)**" to the topic "**Subsite_Lora_Master_Phone**". Replace (number) with the specific line number you would like to test. 
   3) document your findings manually

   **exit**
   ---------------------------------------------------------------------------
   1) send "**exit**" to the topic "**Subsite_Lora_Master_Phone**" to exit out of the current test and be able to choose new tests. You should see "**in menu**" on your phone if you are subscribed to the topic "**Subsite_Lora_To_Phone**". 

    
   **TODO**
   ===========================================================================
   - test each mode and docummenet the lora syntax used for input_thread
   - document public functions and private functions better


   **Public Functions:**
   ===========================================================================
   - **test_all_configurations(test_file, mqtt_master, radio_rn2903):** Use this function for testing all fonigurations (1200+)
   - **test_race_horse(test_file, mqtt_master, radio_rn2903, START_BATCH_NUM = 59, END_BATCH_NUM = 72):** Use this function for fast testing. This function tests only specifc batches and only the highest power level in each batch.
   - **test_manual(test_file, mqtt_master, radio_rn2903):** Use this function to test a specifc config line number. 

    


   **Private Functions:**
   ===========================================================================
   Everything else

       



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   master.create_obj
   master.send_config
   master.find_os
   master.radio_setup
   master.send_data
   master.callback
   master.input_thread
   master.on_connect
   master.on_disconnect
   master.on_message
   master.start_loop_thread
   master.check_message
   master.test_all_configurations
   master.test_race_horse
   master.test_manual
   master.get_line_as_dict
   master.run
   master.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   master.stop_program
   master.mqtt_message
   master.mqtt_topic
   master.distance


.. py:data:: stop_program
   :value: False

   

.. py:data:: mqtt_message
   :value: ''

   

.. py:data:: mqtt_topic
   :value: ''

   

.. py:data:: distance
   :value: 0

   

.. py:function:: create_obj()

   Args:
       - None

   Purpose:
       - Creates he RN2903 object required for using the LoRa device
       - returns the radio object
       - sets the EUI for the LoRa Module as well

   Future additions:
       - be able to use other LoRa Module devices


.. py:function:: send_config(obj, config_line)

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


.. py:function:: find_os()

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


.. py:function:: radio_setup(obj, callback, settings)

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


.. py:function:: send_data(obj, config, config_line)

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



.. py:function:: callback(message)

   Args:
       - message
           * type: hex
           * purpose: containts the infomration from the received LoRa message
   Purpose:
       - decodes the custom header built by Carlos
       - outputs the information received to the terminal 


.. py:function:: input_thread()

   Args:
       - None
   Purpose:
       - stops the program when the user presses a key on the screen



.. py:function:: on_connect(client, userData, flags, rc)

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


.. py:function:: on_disconnect(client, userData, rc)

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


.. py:function:: on_message(client, userData, message)

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



.. py:function:: start_loop_thread(obj)

   Args:
       - obj
           * type: object
           * purpose: able to access the functions in the mqtt class

   Purpose:
       - starts the loop for the MQTT class


.. py:function:: check_message(message, topic)


.. py:function:: test_all_configurations(test_file, mqtt_master, radio_rn2903)

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


.. py:function:: test_race_horse(test_file, mqtt_master, radio_rn2903, START_BATCH_NUM=59, END_BATCH_NUM=72)

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
       - START_BATCH_NUM
           * type: int
           * purpose: the first batch is 0. Feel free to adjust it to test different sections of batches
           * Example: 59 is where sf12 starts on the RN2903 config file
       - END_BATCH_NUM
           * type: int
           * purpose: the last batch is 72. Feel free to adjust it to test differenet sections of batches
       - START
   Purpose:
       - Tests all the first configuration of each possible power level. 
           - sf:12 cr: 4/5 bw: 125kHz pwr: 20
           - sf:12 cr: 4/6 bw: 125kHz pwr: 20
           - sf:12 cr: 4/7 bw: 125kHz pwr: 20
       - Use MQTT conformation to send new newbatches and new messages


.. py:function:: test_manual(test_file, mqtt_master, radio_rn2903)

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
       - test manual configurations
       - if 


.. py:function:: get_line_as_dict(csv_file, line_number)


.. py:function:: run(mqtt_master, radio_rn2903, test_file)

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
           * mode race horse: tests the 72 batch configurations (this is to be updated to make the race horse algorithim faster)
           * mode manual: specify a batch number or config number to your liking
           * mode reset: restarts the menu and you can executre all, test, or manual
           * mode stop: stops the run function and exits


.. py:function:: main()


