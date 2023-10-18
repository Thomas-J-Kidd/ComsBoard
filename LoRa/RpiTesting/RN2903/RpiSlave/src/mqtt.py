import paho.mqtt.client as mqtt

class HiveMQClient:
    def __init__(self, client_id, broker, port=1883):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(self.client_id)

 

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

 

    def on_message(self, client, userdata, msg):
        print(f"Topic: {msg.topic} Message: {msg.payload.decode()}")

 

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)

 

    def subscribe(self, topic):
        self.client.subscribe(topic)

 

    def publish(self, topic, message):
        self.client.publish(topic, message)

 

    def loop_start(self):
        self.client.loop_start()

 

    def loop_stop(self):
        self.client.loop_stop()
