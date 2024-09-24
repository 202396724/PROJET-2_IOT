# voice_recognition.py
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time

# Set up Vosk model for voice recognition
model = Model("C:\\Users\\KARL_12\\PycharmProjects\\progembarquer\\vosk-model-small-fr-0.22")
recognizer = KaldiRecognizer(model, 16000)

# Set up microphone input
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

def listen_for_command():
    """Function to listen for and return recognized voice commands"""
    while True:
        try:
            data = stream.read(4096, exception_on_overflow=False)  # Disable exception on overflow
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                if "text" in result_dict:
                    return result_dict["text"]  # Return the recognized command
        except OSError as e:
            print(f"Error during listening: {e}")
            time.sleep(1)  # Wait before retrying to avoid rapid error cycles
        except Exception as e:
            print(f"Unexpected error: {e}")
            break  # Exit the loop on unexpected errors

def stop_listening():
    """Function to stop the microphone input and cleanup"""
    stream.stop_stream()
    stream.close()
    mic.terminate()

# Usage example (commented out, for reference):
# command = listen_for_command()
# print(f"Recognized command: {command}")
