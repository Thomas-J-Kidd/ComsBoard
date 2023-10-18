:py:mod:`myLibs.Mqtt`
=====================

.. py:module:: myLibs.Mqtt


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   myLibs.Mqtt.MQTTClient




.. py:class:: MQTTClient(client_id, broker='broker.hivemq.com', port=1883, username='None', password='None', on_connect=None, on_disconnect=None, on_message=None, name='None')


   MQTTClient is a class for managing MQTT connections.
   It provides methods for connecting to a broker, subscribing and publishing to topics, and handling MQTT events.

   .. py:method:: connect()

      Connect to the MQTT broker.

      :return: True if the connection succeeded, False otherwise.


   .. py:method:: disconnect()

      Disconnect from the MQTT broker.

      :return: True if the disconnection succeeded, False otherwise.


   .. py:method:: subscribe(topic)

      Subscribe to a topic.

      :param topic: The topic to subscribe to.
      :return: True if the subscription succeeded, False otherwise.


   .. py:method:: unsubscribe(topic)

      Unsubscribe from a topic.

      :param topic: The topic to unsubscribe from.
      :return: True if the unsubscription succeeded, False otherwise.


   .. py:method:: publish(topic, message)

      Publish a message to a topic.

      :param topic: The topic to publish the message to.
      :param message: The message to publish.
      :return: True if the publish succeeded, False otherwise.


   .. py:method:: on_connect(client, userdata, flags, rc)

      Handle the connect event.

      :param client: The client instance for this callback.
      :param userdata: The private user data as set in Client() or userdata_set().
      :param flags: Response flags sent by the broker.
      :param rc: The connection result.


   .. py:method:: on_disconnect(client, userdata, rc)

      Handle the disconnect event.

      :param client: The client instance for this callback.
      :param userdata: The private user data as set in Client() or userdata_set().
      :param rc: The disconnection result.


   .. py:method:: on_message(client, userdata, message)

      Handle the message event.

      :param client: The client instance for this callback.
      :param userdata: The private user data as set in Client() or userdata_set().
      :param message: An instance of MQTTMessage.


   .. py:method:: on_publish(client, userdata, mid)

      Handle the publish event.

      :param client: The client instance for this callback.
      :param userdata: The private user data as set in Client() or userdata_set().
      :param mid: Matches the mid variable returned from the corresponding publish() call, to allow outgoing messages to be tracked.


   .. py:method:: loop_start()

      Start the MQTT client's network loop in a new thread.

      :return: True if the loop started successfully, False otherwise.


   .. py:method:: loop_stop()

      Stop the MQTT client's network loop.

      :return: True if the loop stopped successfully, False otherwise.


   .. py:method:: get_subscriptions()

      Get a list of all current subscriptions.

      :return: A list of all current subscriptions.


   .. py:method:: get_publications()

      Get a list of all topics this client has published to.

      :return: A list of all topics this client has published to.



