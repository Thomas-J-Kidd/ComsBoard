:py:mod:`src.slavev2`
=====================

.. py:module:: src.slavev2


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   src.slavev2.on_connect_callback
   src.slavev2.on_disconnect_callback
   src.slavev2.on_message_callback
   src.slavev2.send_config
   src.slavev2.callback
   src.slavev2.create_array
   src.slavev2.save_to_csv
   src.slavev2.add_new_data_to_csv
   src.slavev2.restart_array
   src.slavev2.check_for_ones
   src.slavev2.find_os
   src.slavev2.radio_setup
   src.slavev2.rec_loop_mqtt
   src.slavev2.start_mqtt_receive
   src.slavev2.mqtt_send



Attributes
~~~~~~~~~~

.. autoapisummary::

   src.slavev2.red
   src.slavev2.green
   src.slavev2.yellow
   src.slavev2.blue
   src.slavev2.reset
   src.slavev2.port
   src.slavev2.settings
   src.slavev2.radio_rn2903
   src.slavev2.mqttClient
   src.slavev2.batch_config_file
   src.slavev2.all_configs_file
   src.slavev2.received_configs_array
   src.slavev2.configurations
   src.slavev2.userIn


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


.. py:function:: send_config(obj, config_line)

   Send the new configuration to the device

   Args:
   - obj: The radio object that the configuration is for
   - config_line: The new configuration to be sent to the module



.. py:function:: callback(message)


.. py:function:: create_array(file)


.. py:function:: save_to_csv(df, file)

   Saves a pandas dataframe to a .csv file

   Args:
   - df: the pandas dataframe that you want to save
   - file: the filename you want to save the dataframe to



.. py:function:: add_new_data_to_csv(file, distance, array)

   Adds the pass/fail data to the .csv file with the name
   of the column being the distance that was decided by the master

   Args:
   - file: the filename that you want to save the new data to
   - distance: the distance or name you want the column to have



.. py:function:: restart_array(array)


.. py:function:: check_for_ones(array)


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

   

.. py:data:: received_configs_array

   

.. py:data:: configurations

   

.. py:data:: userIn

   

