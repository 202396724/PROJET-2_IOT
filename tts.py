import pyttsx3

class TTS:
    def __init__(self):
        # Initialize the speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.last_text = ""

    def setup_voice(self):
        # Get the list of available voices and set a French voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "french" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 150)  # Speech rate
        self.engine.setProperty('volume', 1)   # Volume level

    def speak(self, text):
        if text and text != self.last_text:
            self.last_text = text
            self.engine.say(text)
            self.engine.runAndWait()

# Optionally, for testing:
if __name__ == "__main__":
    tts = TTS()
    tts.speak("Bonjour, ceci est un test.")

#### DO NOT MODIFY THIS FILE ####
