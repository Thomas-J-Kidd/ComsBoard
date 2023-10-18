:py:mod:`RYLR998_sender`
========================

.. py:module:: RYLR998_sender


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   RYLR998_sender.radio_setup
   RYLR998_sender.callback
   RYLR998_sender.on_connect_callback
   RYLR998_sender.on_disconnect_callback
   RYLR998_sender.on_message_callback
   RYLR998_sender.rec_loop_mqtt
   RYLR998_sender.start_mqtt_receive
   RYLR998_sender.mqtt_send



Attributes
~~~~~~~~~~

.. autoapisummary::

   RYLR998_sender.red
   RYLR998_sender.green
   RYLR998_sender.yellow
   RYLR998_sender.reset
   RYLR998_sender.blue
   RYLR998_sender.settings
   RYLR998_sender.radio
   RYLR998_sender.mqttClient
   RYLR998_sender.configuration
   RYLR998_sender.userIn


.. py:data:: red
   :value: '\x1b[91m'

   

.. py:data:: green
   :value: '\x1b[92m'

   

.. py:data:: yellow
   :value: '\x1b[93m'

   

.. py:data:: reset
   :value: '\x1b[0m'

   

.. py:data:: blue
   :value: '\x1b[94m'

   

.. py:function:: radio_setup(callback, settings)

   Sets up the radio object and starts the serial threads

   Args:
   - callback: The callback function that alerts you of a new message
   - settings: The initial port and buffer settings



.. py:function:: callback(message)


.. py:data:: settings

   

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


.. py:function:: rec_loop_mqtt()

   Starts the receive loop for the MQTT, allowing for continuous MQTT message receival

   Args: 
   none



.. py:function:: start_mqtt_receive(obj, threadName=rec_loop_mqtt, topic='RYLR998')

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



.. py:data:: radio

   

.. py:data:: mqttClient

   

.. py:data:: configuration

   

.. py:data:: userIn

   

