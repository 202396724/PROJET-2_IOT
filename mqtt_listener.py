import paho.mqtt.client as mqtt
from tts import TTS

# Create a TTS instance
tts = TTS()

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    print(f"Received message: {msg}")
    tts.speak(msg)

# MQTT configurations
broker = "test.mosquitto.org"  # Replace with your broker address
port = 1883                           # Default MQTT port
topic = "LOGGING/vers-pc"             # Replace with your topic

# Create an MQTT client instance
client = mqtt.Client()
client.on_message = on_message

# Connect to the broker with specified port and keep-alive interval
client.connect(broker, port, 60)
client.subscribe(topic)

# Start the MQTT loop
client.loop_forever()
