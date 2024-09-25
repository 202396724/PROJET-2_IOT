import paho.mqtt.client as mqtt
from pymongo import MongoClient
from tts_2 import TTS
from datetime import datetime  # Import datetime

# Create a TTS instance
tts = TTS()

# MongoDB configurations
mongo_client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
db = mongo_client['DONNEES']  # Replace with your database name
collection = db['MOUVEMENT_ALERTE']  # Replace with your collection name

# Mapping des messages MONGODB et PYTTSX3
message_mapping = {
    "Mode normal actif": "Le systeme passe au mode normal",
    "Mode pieton actif": "Les feux passent au rouge pour les pietons",
    "Mode panne actif": "Les feux rouges clignotent des deux cotes",
    "Mode urgence actif": "Les feux verts s'allument dans la direction d'urgence",
    "Commande non reconnue": "Aucun changement d'etat, commande erroner."
}

# Functions for handling each specific message
def handle_message1():
    print("Handling message 1")

def handle_message2():
    print("Handling message 2")

def handle_message3():
    print("Handling message 3")

def handle_message4():
    print("Handling message 4")

def handle_message5():
    print("Handling message 5")

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    print(f"On a recu le message!: {msg}")

    # Speak the received message
    try:
        tts.speak(msg)
    except Exception as e:
        print(f"On a une erreur au niveau TTS: {e}")

    # Map the received message to a new message
    mapped_msg = message_mapping.get(msg, "unknown")  # Default to "unknown" if not found

    # Create the new message for the database
    db_msg = f"{mapped_msg}"

    # Get the current timestamp
    timestamp = datetime.now()  # Current date and time

    # Insert the new message into MongoDB with timestamp
    collection.insert_one({'message': db_msg, 'timestamp': timestamp})
    print(f"On a inserer: {db_msg} dans mongodb avec le timestamp: {timestamp}")

    # Call the appropriate handler based on the message
    if msg == "message1":
        handle_message1()
    elif msg == "message2":
        handle_message2()
    elif msg == "message3":
        handle_message3()
    elif msg == "message4":
        handle_message4()
    elif msg == "message5":
        handle_message5()

    # Pour garder 5 message max :
    if collection.count_documents({}) > 5:
        oldest_message = collection.find_one(sort=[('_id', 1)])  # on retrouve le message le plus vieux
        if oldest_message:
            collection.delete_one({'_id': oldest_message['_id']})  # on enleve le plus vieux message
            print(f"C'est le 5ieme! On enleve: {oldest_message['message']}")

# MQTT configurations
broker = "test.mosquitto.org"  # addresse broker
port = 1883  # port par default
topic = "LOGGING/vers-pc"  # topic et sous topic

# Create an MQTT client instance
client = mqtt.Client()
client.on_message = on_message

# Connect to the broker with specified port and keep-alive interval
client.connect(broker, port, 60)
client.subscribe(topic)

# Start the MQTT loop
client.loop_forever()
