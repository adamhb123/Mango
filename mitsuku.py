#!/usr/bin/env python3

# Distributed under the MIT License.

"""
[NEW]
This was modified by me (Adam Brewer) for use with my "robot".
Just modified some small stuff, most of the credit for this
goes to https://github.com/hanwenzhu/

I've rendered the documentation below somewhat useless with the
modifications that I've made.


[OLD]
An API for Mitsuku[https://www.pandorabots.com/mitsuku/], a chatbot.

This is _not_ official.  It's just a little project that I'm working
on.  Usage:
```sh
python3 main.py [file]
```
file: input to chatbot.  If not found, you will enter it in stdin.

As for now, it just outputs the response to stdout.

You need the following stuff for it to work:
- Any distribution of Python, version 3.6 or above
- beautifulsoup4
- lxml
- requests
- Internet access
"""
from dataclasses import dataclass
import json
import random
import re
import sys
import urllib.parse
import bs4
import requests
import time
from warnings import filterwarnings
from threading import Thread
import pyttsx3

_HELP_MSG = "\n[HELP]\n" + ''.join(open('help', 'r').readlines())


class SpeechEngine:
    def __init__(self):
        self._engine = pyttsx3.init()
        self.setProperty = self._engine.setProperty
        self.getProperty = self._engine.getProperty
        self.runAndWait = self._engine.runAndWait

    def say(self, text, print_text=True, name=None):
        #   Change Kuki to Mango for aesthetics:tm:
        text.replace('Kuki', 'Mango')
        text.replace('kuki', 'mango')
        self._engine.say(text, name)
        if print_text: print(text)


class Mitsuku:
    def __init__(self, voice_id=None, voice_rate=None, voice_volume=None, say_response: bool = True):
        self.say_response = say_response
        self.load_bot()
        #   Some cute aliases
        self.reload, self.reload_bot = self.load_bot, self.load_bot

        self.speech_engine = SpeechEngine()
        self.voices = self.speech_engine.getProperty('voices')
        self.formatted_voices = []
        for voice in self.voices:
            self.formatted_voices.append(f"{voice.id} {voice.gender}")
            print(f"voice.id = {voice.id} voice_id = {voice_id} EQUAL: {voice.id == voice_id}")
            if voice_id is not None and voice_id.strip() == voice.id.strip():
                self.speech_engine.setProperty('voice', voice.id)
                self.speech_engine.say(f"Set speech_engine voice to {voice.id}")
                self.speech_engine.runAndWait()

        if voice_rate is not None:
            self.speech_engine.setProperty('rate', voice_rate)
        if voice_volume is not None:
            self.speech_engine.setProperty('volume', voice_volume)
        self.speech_engine.say(f"Booting up! My current voice is: {self.speech_engine.getProperty('voice')}")
        self.speech_engine.runAndWait()

    def load_bot(self):
        url = 'https://www.pandorabots.com/mitsuku/'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': ' '.join(('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2)',
                                    'AppleWebKit/537.36 (KHTML, like Gecko)',
                                    'Chrome/72.0.3626.119 Safari/537.36')),
            'Referer': url
        })

        self.main_page = self.session.get(url).text
        self.main_soup = bs4.BeautifulSoup(self.main_page, 'lxml')
        self.botkey = re.search(r'PB_BOTKEY: "(.*)"', self.main_page).groups()[0]

        # Mitsuku does not check your client_name really carefully (smirk) as
        # long as the length is 13.
        self.client_name = str(random.randint(1337, 9696913371337)).rjust(13, '0')
        print("Bot loaded")

    def change_voice_interactively(self):
        voice = int(input(f"Choose a voice type(0 -> {len(self.voices) - 1}): "))
        rate = int(input("Choose a speaking rate: "))
        volume = float(input("Choose a volume (0.0 -> 1.0): "))
        self.speech_engine.setProperty('voice', voice)
        self.speech_engine.setProperty('rate', rate)
        self.speech_engine.setProperty('volume', volume if 0 <= volume <= 1 else 1)
        # self.speech_engine.setProperty('voice', self.raw_voices[gender])

    def handle_config(self, query) -> str:
        query = query.replace(':', '').split()
        if len(query) != 1:
            return self.say("Setting modification query is invalid!")
        else:
            command = query[0].split('=')
            if command[0] == "set_voice":
                self.change_voice_interactively()
            elif command[0] == "get_voices":
                return self.formatted_voices
            elif command[0] == "help":
                return _HELP_MSG
            else:
                return self.respond("Setting modification query is invalid!")

    def get_response(self, query: str) -> str:
        if len(query) == 0:
            return self.respond("Setting modification query is invalid!")
        if query[0] == ':':
            return self.handle_config(query)

        initial_query = query
        query = re.sub(r'\s+', ' ', query).strip()
        query = urllib.parse.quote(query)

        response_raw = self.session.post(
            f'https://miapi.pandorabots.com/talk?'
            f'botkey={self.botkey}&'
            f'input={query}&'
            f'client_name={self.client_name}&'
            f'sessionid=null&'
            f'channel=6').text
        try:
            response_json = json.loads(response_raw)
        except json.JSONDecodeError:
            # Sometimes Mitsuku sends stuff like pictures.
            response_json = {'responses': ["<i can't understand it, bro>"]}
        # If the query is too long, Mitsuku answers in several lines.  Here
        # I'll just put it into paragraphs.
        if '{"status": "error"' in response_json['responses'][0]:
            self.reload()
            return self.get_response(initial_query)
        response = '\n\n'.join(response_json['responses'])
        if self.say_response:
            self.respond(response)
        self.speech_engine.runAndWait()
        return response


def mitsuku_test(oneshot_query: str = None):
    mitsu = Mitsuku()
    if oneshot_query:
        print(mitsu.get_response(oneshot_query))
    else:
        while True:
            query = input("Say: ")
            print(mitsu.get_response(query))


if __name__ == "__main__":
    mitsuku_test()
