import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import ssl
import json


load_dotenv()

"""# Assume 'access_token' is a variable holding your obtained token
access_token = os.getenv("password")
mqtt_broker = "mqtt.openf1.org"
mqtt_port = 8883

# Optional: Provide a username. Can be an email or any non-empty string.
mqtt_username = os.getenv("username")

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to OpenF1 MQTT broker")
        client.subscribe("v1/location")
        client.subscribe("v1/laps")
        # client.subscribe("#") # Subscribe to all topics
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username=mqtt_username, password=access_token)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever() # Starts a blocking network loop
except Exception as e:
    print(f"Connection error: {e}")
"""

#Trying in Class format

class Live_OpenF1:
    def __init__(self):
        self.mqtt_username = os.getenv("username")
        self.access_token = os.getenv("password")
        self.mqtt_broker = "mqtt.openf1.org"
        self.mqtt_port = 8883

    def setup(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(username=self.mqtt_username, password=self.access_token)
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
            self.client.loop_forever() # Starts a blocking network loop
        except Exception as e:
            print(f"Connection error: {e}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to OpenF1 MQTT broker")
            self.client.subscribe("v1/location")
            self.client.subscribe("v1/laps")
            # client.subscribe("#") # Subscribe to all topics
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
        data = json.loads(msg.payload.decode())


live_data = Live_OpenF1()
data = live_data.setup()