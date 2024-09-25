import tkinter as tk
import threading
import paho.mqtt.client as mqtt
from vosk_voice import listen_for_command  # Import du module vosk

# Variable pour indiquer si le système doit écouter ou non
listening = False
listening_thread = None  # Variable pour stocker le thread d'écoute

# Initialiser le client MQTT
client = mqtt.Client()

# MQTT callback lorsqu'une confirmation est reçue (facultatif)
def on_message(client, userdata, message):
    confirmation = message.payload.decode('utf-8')
    print(f"Received confirmation: {confirmation}")

# Configurer le client MQTT pour écouter les confirmations (facultatif)
client.on_message = on_message
client.connect('test.mosquitto.org', 1883)
client.loop_start()

# Dictionnaire de traitement des commandes
commands = {
    "activez mode normal": "Mode normal activé",
    "passez au mode piétons": "Mode piéton activé",
    "passez en mode panne": "Mode panne activé",
    "activez le mode urgence": "Mode urgence activé",
}

def process_command(command_text):
    command_text = command_text.lower()
    response = commands.get(command_text, "Commande non reconnue")
    client.publish('LOGIC/vers-rasp', command_text)  # Publier la commande telle quelle
    print(f"Processed command: {command_text} -> {response}")

# Fonction pour gérer l'écoute des commandes
def start_listening():
    global listening
    print("Listening for commands...")
    while listening:
        command_text = listen_for_command()  # appel de la fonction depuis le module vosk_voice
        print(f"Recognized command: {command_text}")
        process_command(command_text)

# Fonction qui gère le bouton pour commencer/arrêter l'écoute
def toggle_listening():
    global listening, listening_thread
    listening = not listening
    if listening:
        button.config(text="Arrêter l'écoute")
        # Démarrer l'écoute dans un thread séparé
        listening_thread = threading.Thread(target=start_listening)
        listening_thread.start()
    else:
        button.config(text="Commencer l'écoute")
        listening = False  # Arrêter l'écoute
        if listening_thread is not None:
            listening_thread.join()  # Attendre que le thread se termine
            listening_thread = None  # Réinitialiser le thread d'écoute

# Création de l'interface avec Tkinter
root = tk.Tk()
root.title("Commande vocale")

# Création du bouton pour démarrer/arrêter l'écoute
button = tk.Button(root, text="Commencer l'écoute", command=toggle_listening)
button.pack(pady=20)

# Lancement de la boucle Tkinter
root.mainloop()
