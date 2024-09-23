import paho.mqtt.client as mqtt
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from pymongo import MongoClient
from datetime import datetime

# Initialize the MQTT client
client = mqtt.Client()

# Connect to MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['traffic_light_system']
commands_collection = db['commands']

# Set up voice engine (pyttsx3)
engine = pyttsx3.init()

# Set up Vosk model for voice recognition
model = Model("C:\Users\KARL_12\PycharmProjects\progembarquer\vosk-model-small-fr-0.22 2")
recognizer = KaldiRecognizer(model, 16000)

# Set up microphone input
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


# Function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to save the command in MongoDB
def save_command(command, response):
    if commands_collection.count_documents({}) >= 5:
        # Remove the oldest command
        commands_collection.find_one_and_delete({}, sort=[('_id', 1)])

    commands_collection.insert_one({
        "command": command,
        "response": response,
        "timestamp": datetime.now()
    })


# MQTT callback when the command is confirmed
def on_message(client, userdata, message):
    confirmation = message.payload.decode('utf-8')
    speak(confirmation)
    print(f"Received confirmation: {confirmation}")


# Set up MQTT client to listen for confirmations
client.on_message = on_message
client.connect('localhost', 1883)
client.subscribe('traffic_light/confirmation')
client.loop_start()

# Command processing
commands = {
    "activer mode normal": "Mode normal activé",
    "passer au mode piéton": "Mode piéton activé",
    "passer en mode panne": "Mode panne activé",
    "activer le mode urgence": "Mode urgence activé"
}


def process_command(command_text):
    command_text = command_text.lower()
    response = commands.get(command_text, "Commande non reconnue")

    # Publish the command to MQTT
    client.publish('traffic_light/command', command_text)

    # Provide vocal feedback
    speak(response)

    # Save the command in MongoDB
    save_command(command_text, response)

    print(f"Processed command: {command_text} -> {response}")


# Voice recognition loop
print("Listening for commands...")
while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result_dict = json.loads(result)
        if "text" in result_dict:
            command_text = result_dict["text"]
            print(f"Recognized command: {command_text}")
            process_command(command_text)
