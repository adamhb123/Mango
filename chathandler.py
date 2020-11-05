# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from mitsuku import Mitsuku
import time


class ChatHandler:
    def __init__(self, voice_id=None, voice_rate=None, voice_volume=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.mitsuku = Mitsuku(voice_id=voice_id,
                               voice_rate=voice_rate,
                               voice_volume=voice_id)
        self.mitsuku.respond("Adjusting for ambient noise...please be quiet...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Done adjusting for ambient noise!")

    def main_loop(self):
        while True:
            print("Speak!")
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=2)
                text = self.recognizer.recognize_google(audio)
                config_check = text.strip().replace(' ', '')
                # if config_check == "changevoicerateto":

                print(f"You said '{text}'")
                print(self.mitsuku.get_response(text))

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except sr.WaitTimeoutError:
                pass
