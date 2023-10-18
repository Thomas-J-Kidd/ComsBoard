import paho.mqtt.client as mqtt
from . import Debug

class MQTTClient:
    """
    MQTTClient is a class for managing MQTT connections.
    It provides methods for connecting to a broker, subscribing and publishing to topics, and handling MQTT events.
    """
    def __init__(self, client_id, broker="broker.hivemq.com", port=1883, username="None", password="None", on_connect=None, on_disconnect=None, on_message=None, name="None"):
        """
        Initialize the MQTTClient.
        
        :param client_id: The unique identifier for this client.
        :param broker: The address of the MQTT broker to connect to.
        :param port: The port to use for the connection.
        :param username: The username to use for authentication.
        :param password: The password to use for authentication.
        :param on_connect: A callback for when the client connects.
        :param on_disconnect: A callback for when the client disconnects.
        :param on_message: A callback for when a message is received.
        :param name: The name of this client for debugging purposes.
        """
        self.name = name
        self.pd = Debug.prettyDebug(name=self.name)
        self.pd.LOCAL_DEBUG = False
        self.pd.LOCAL_LOG = False
        self.pd.print("INIT")
        
        self.client = mqtt.Client(client_id)
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.on_connect_cb = on_connect
        self.on_message_cb = on_message
        self.on_disconnect_cb = on_disconnect
        
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

        self.subscriptions = []
        self.publications = []

    def connect(self):
        """
        Connect to the MQTT broker.

        :return: True if the connection succeeded, False otherwise.
        """
        try:
            self.client.connect(self.broker, self.port)
            self.pd.print("Connected")
        except Exception as e:
            self.pd.print(f"Connect: Failed to connect to MQTT broker: {e}")
            return False
        return True

    def disconnect(self):
        """
        Disconnect from the MQTT broker.

        :return: True if the disconnection succeeded, False otherwise.
        """
        try:
            self.client.disconnect()
            self.pd.print("Disconnected")
        except Exception as e:
            self.pd.print(f"Disconnect: Failed to disconnect from MQTT broker: {e}")
            return False
        return True

    def subscribe(self, topic):
        """
        Subscribe to a topic.

        :param topic: The topic to subscribe to.
        :return: True if the subscription succeeded, False otherwise.
        """
        try:
            self.client.subscribe(topic)
            if topic not in self.subscriptions:
                self.pd.print(f"Subscribing to topic: {topic}")
                self.subscriptions.append(topic)
        except Exception as e:
            self.pd.print(f"subscribe: Failed to subscribe to topic {topic}: {e}")
            return False
        return True

    def unsubscribe(self, topic):
        """
        Unsubscribe from a topic.

        :param topic: The topic to unsubscribe from.
        :return: True if the unsubscription succeeded, False otherwise.
        """
        try:
            self.client.unsubscribe(topic)
            if topic in self.subscriptions:
                self.pd.print(f"Unsubscribing from topic: {topic}")
                self.subscriptions.remove(topic)
        except Exception as e:
            self.pd.print(f"unsubscribe: Failed to unsubscribe from topic {topic}: {e}")
            return False
        return True

    def publish(self, topic, message):
        """
        Publish a message to a topic.

        :param topic: The topic to publish the message to.
        :param message: The message to publish.
        :return: True if the publish succeeded, False otherwise.
        """
        try:
            self.client.publish(topic, message)
            self.pd.print(f"Publishing to topic: {topic} - Message: {message}")
            if topic not in self.publications:
                self.publications.append(topic)
        except Exception as e:
            self.pd.print(f"publish: Failed to publish message to topic {topic}: {e}")
            return False
        return True

    def on_connect(self, client, userdata, flags, rc):
        """
        Handle the connect event.

        :param client: The client instance for this callback.
        :param userdata: The private user data as set in Client() or userdata_set().
        :param flags: Response flags sent by the broker.
        :param rc: The connection result.
        """
        if rc != 0:
            self.pd.print(f"on_connect: Connection failed with error code {rc}")
        elif self.on_connect_cb is not None:
            self.on_connect_cb(client, userdata, flags, rc)

    def on_disconnect(self, client, userdata, rc):
        """
        Handle the disconnect event.

        :param client: The client instance for this callback.
        :param userdata: The private user data as set in Client() or userdata_set().
        :param rc: The disconnection result.
        """
        if rc != 0:
            self.pd.print(f"on_disconnect: Unexpected disconnection.")
        self.subscriptions.clear()
        self.publications.clear()
        if self.on_disconnect_cb is not None:
            self.on_disconnect_cb(client, userdata, rc)

    def on_message(self, client, userdata, message):
        """
        Handle the message event.

        :param client: The client instance for this callback.
        :param userdata: The private user data as set in Client() or userdata_set().
        :param message: An instance of MQTTMessage.
        """
        if self.on_message_cb is not None:
            self.on_message_cb(client, userdata, message)
        else:
            self.pd.print(f"on_message: {message.payload.decode()} on topic {message.topic}")

    def on_publish(self, client, userdata, mid):
        """
        Handle the publish event.

        :param client: The client instance for this callback.
        :param userdata: The private user data as set in Client() or userdata_set().
        :param mid: Matches the mid variable returned from the corresponding publish() call, to allow outgoing messages to be tracked.
        """
        self.pd.print(f"on_publish: Message {mid} delivered")

    def loop_start(self):
        """
        Start the MQTT client's network loop in a new thread.

        :return: True if the loop started successfully, False otherwise.
        """
        try:
            self.client.loop_start()
        except Exception as e:
            self.pd.print(f"loop_start: Failed to start loop: {e}")
            return False
        return True

    def loop_stop(self):
        """
        Stop the MQTT client's network loop.

        :return: True if the loop stopped successfully, False otherwise.
        """
        try:
            self.client.loop_stop()
        except Exception as e:
            self.pd.print(f"loop_stop: Failed to stop loop: {e}")
            return False
        return True

    def get_subscriptions(self):
        """
        Get a list of all current subscriptions.

        :return: A list of all current subscriptions.
        """
        return self.subscriptions

    def get_publications(self):
        """
        Get a list of all topics this client has published to.

        :return: A list of all topics this client has published to.
        """
        return self.publications
