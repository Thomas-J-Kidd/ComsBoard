:py:mod:`src.slave`
===================

.. py:module:: src.slave


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   src.slave.on_connect_callback
   src.slave.on_disconnect_callback
   src.slave.on_message_callback
   src.slave.send_config
   src.slave.callback
   src.slave.save_to_csv
   src.slave.add_new_data_to_csv
   src.slave.restart_array
   src.slave.check_for_successes
   src.slave.find_os
   src.slave.radio_setup
   src.slave.rec_loop_mqtt
   src.slave.start_mqtt_receive
   src.slave.mqtt_send



Attributes
~~~~~~~~~~

.. autoapisummary::

   src.slave.red
   src.slave.green
   src.slave.yellow
   src.slave.blue
   src.slave.reset
   src.slave.port
   src.slave.settings
   src.slave.radio_rn2903
   src.slave.mqttClient
   src.slave.batch_config_file
   src.slave.all_configs_file
   src.slave.configurations
   src.slave.received_messages_array
   src.slave.userIn


.. py:data:: red
   :value: '\x1b[91m'

   

.. py:data:: green
   :value: '\x1b[92m'

   

.. py:data:: yellow
   :value: '\x1b[93m'

   

.. py:data:: blue
   :value: '\x1b[94m'

   

.. py:data:: reset
   :value: '\x1b[0m'

   

.. py:function:: on_connect_callback(client, userdata, flags, rc)

   Callback for handling the MQTT connect event

   Args:
   - client: the client instace for the callback
   - userdata: the private user data as set in Client() or userdata_set()
   - flags: response flags sent by the broker
   - rc: the connection result



.. py:function:: on_disconnect_callback(client, userdata, rc)

   callback for handling the MQTT disconnect event.

   Args: 
   - client: The client instance for this callback.
   - userdata: The private user data as set in Client() or userdata_set().
   - rc: The disconnection result.


.. py:function:: on_message_callback(client, userdata, message)

   Handle the message event and perform different funcions
   according to the message

   Args:
   - client: The client instance for this callback.
   - userdata: The private user data as set in Client() or userdata_set().
   - message: An instance of MQTTMessage.


.. py:function:: send_config(obj, config_line)

   Send the new configuration to the device

   Args:
   - obj: The radio object that the configuration is for
   - config_line: The new configuration to be sent to the module



.. py:function:: callback(message)

   Handles new messages from the module

   Args:
   - message: the message that is received from the module



.. py:function:: save_to_csv(df, file)

   Saves a pandas dataframe to a .csv file

   Args:
   - df: the pandas dataframe that you want to save
   - file: the filename you want to save the dataframe to



.. py:function:: add_new_data_to_csv(file, distance)

   Adds the pass/fail data to the .csv file with the name
   of the column being the distance that was decided by the master

   Args:
   - file: the filename that you want to save the new data to
   - distance: the distance or name you want the column to have



.. py:function:: restart_array(array)


.. py:function:: check_for_successes(file)

   Iterates through the collected data and returns an array 
   of all configuration lines that were successful

   Args:
   - file: The .csv file that we are checking for successful transmissions in



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


.. py:function:: radio_setup(callback, settings)

   Sets up the radio object and starts the serial threads

   Args:
   - callback: The callback function that alerts you of a new message
   - settings: The initial port and buffer settings



.. py:function:: rec_loop_mqtt()

   Starts the receive loop for the MQTT, allowing for continuous MQTT message receival

   Args: 
   none



.. py:function:: start_mqtt_receive(obj, threadName=rec_loop_mqtt, topic='Subsite_Lora_Master')

   Subscribes to the topic you want to receive messages from via MQTT
   and starts the thread for continuous MQTT receival

   Args:
   - obj: the MQTT object
   - threadname: the name of the function that initiates the loop for MQTT receiving
   - topic: the topic that you want to subscribe to



.. py:function:: mqtt_send(obj, topic, message)

   Sends a message to a particular topic via MQTT

   - obj: the MQTT object
   - topic: the topic that you want to publish the message to
   - message: the message that you want to publish



.. py:data:: port

   

.. py:data:: settings

   

.. py:data:: radio_rn2903

   

.. py:data:: mqttClient

   

.. py:data:: batch_config_file
   :value: 'csv/module_configurations_slave.csv'

   

.. py:data:: all_configs_file
   :value: 'csv/module_configurations.csv'

   

.. py:data:: configurations

   

.. py:data:: received_messages_array
   :value: []

   

.. py:data:: userIn

   

