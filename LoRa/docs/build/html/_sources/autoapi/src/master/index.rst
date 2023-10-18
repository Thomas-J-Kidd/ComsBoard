:py:mod:`src.master`
====================

.. py:module:: src.master

.. autoapi-nested-parse::

   @package docstring
   Documentation for this module.
    
   More details.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   src.master.create_obj
   src.master.send_config
   src.master.find_os
   src.master.radio_setup
   src.master.send_data
   src.master.callback
   src.master.input_thread
   src.master.on_connect
   src.master.on_disconnect
   src.master.on_message
   src.master.start_loop_thread
   src.master.check_message
   src.master.test_all_configurations
   src.master.test_race_horse
   src.master.test_manual
   src.master.get_line_as_dict
   src.master.run
   src.master.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   src.master.stop_program
   src.master.mqtt_message
   src.master.mqtt_topic


.. py:data:: stop_program
   :value: False

   

.. py:data:: mqtt_message
   :value: ''

   

.. py:data:: mqtt_topic
   :value: ''

   

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


.. py:function:: test_race_horse(test_file, mqtt_master, radio_rn2903)


.. py:function:: test_manual(test_file, mqtt_master, radio_rn2903)


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
           * mode test: tests the 72 batch configurations (this is to be updated to make the race horse algorithim faster)
           * mode manual: specify a batch number or config number to your liking
           * mode reset: restarts the menu and you can executre all, test, or manual
           * mode stop: stops the run function and exits


.. py:function:: main()


