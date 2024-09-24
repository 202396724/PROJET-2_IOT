import paho.mqtt.client as mqtt
import pyttsx3
from vosk_voice_recongnition import listen_for_command  # Import du module vosk

# Initialize the MQTT client
client = mqtt.Client()

# Set up voice engine (pyttsx3)
engine = pyttsx3.init()

# Function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

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
    "activez mode normal": "Mode normal activé",
    "passez au mode piétons": "Mode piéton activé",
    "passez en mode panne": "Mode panne activé",
    "activez le mode urgence": "Mode urgence activé",
}

def process_command(command_text):
    command_text = command_text.lower()
    response = commands.get(command_text, "Commande non reconnue")

    # Publish the command to MQTT (common topic: 'traffic_light/mode')
    client.publish('traffic_light/mode', command_text)

    # Provide vocal feedback
    speak(response)

    print(f"Processed command: {command_text} -> {response}")

# Main loop to activate voice control
print("Listening for commands...")
while True:
    command_text = listen_for_command()  # appel de la fonction depuis le module vosk_voice_recongnition
    print(f"Recognized command: {command_text}")
    process_command(command_text)
