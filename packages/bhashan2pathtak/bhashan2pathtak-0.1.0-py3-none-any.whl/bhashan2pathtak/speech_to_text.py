import sys
import re

if sys.version_info >= (3, 12):
    class LooseVersion:
        component_re = re.compile(r'(\d+ | [a-z]+ | \.)', re.VERBOSE)

        def __init__(self, vstring):
            self.vstring = vstring
            self.version = self._parse(vstring)

        def _parse(self, vstring):
            components = [x for x in self.component_re.split(vstring) if x and x != '.']
            for i, obj in enumerate(components):
                try:
                    components[i] = int(obj)
                except ValueError:
                    pass
            return components

        def __str__(self):
            return self.vstring

        def __repr__(self):
            return f"LooseVersion ('{self.vstring}')"

        def __eq__(self, other):
            return self.version == other.version

        def __lt__(self, other):
            return self.version < other.version

        def __le__(self, other):
            return self.version <= other.version

        def __gt__(self, other):
            return self.version > other.version

        def __ge__(self, other):
            return self.version >= other.version


    sys.modules['distutils.version'] = type('', (), {'LooseVersion': LooseVersion})()

import speech_recognition as sr
from wit import Wit
import os
import json


def load_config():
    # Try to load from config file first
    try:
        with open('../../config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}


def get_wit_token():
    # Try to get token from environment variable first
    token = os.environ.get('WIT_AI_TOKEN')
    if token:
        return token

    # If not in environment, try to get from config file
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            token = config.get('WIT_AI_TOKEN')
            if token:
                return token
    except FileNotFoundError:
        pass

        # If still no token, guide the user
    print("Wit.ai token not found. Please follow these steps to set up your token:")
    print("1. Go to https://wit.ai/ and create an account if you haven't already.")
    print("2. Create a new Wit.ai app and copy your Client Access Token.")
    print("3. Set your token using one of these methods:")
    print("   a. Set an environment variable:")
    print("      export WIT_AI_TOKEN=your_token_here")
    print("   b. Create a config.json file in the current directory with the following content:")
    print("      {\"WIT_AI_TOKEN\": \"your_token_here\"}")
    print("\nAfter setting up your token, run this program again.")
    sys.exit(1)

def transcribe_wit(audio_data, wit_client):
    try:
        result = wit_client.speech(audio_data, {'Content-Type': 'audio/wav'})
        return result['text']
    except Exception as e:
        print(f"Wit.ai error: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response content: {e.response.content}")
        return None


def main():
    wit_token = get_wit_token()
    if not wit_token:
        print("Error: WIT_AI_TOKEN not found in environment variables or config file")
        print("Please set the WIT_AI_TOKEN environment variable or create a config.json file")
        return

    recognizer = sr.Recognizer()
    wit_client = Wit(wit_token)

    # Adjust these parameters as needed
    phrase_time_limit = 15  # Maximum number of seconds for a phrase

    with sr.Microphone() as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 4000  # Adjust this value based on your environment
        print("Ambient noise adjustment complete.")

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=phrase_time_limit)

                print("Processing...")
                wav_data = audio.get_wav_data(
                    convert_rate=16000,  # Wit.ai requires 16kHz sample rate
                    convert_width=2  # 16-bit depth
                )
                text = transcribe_wit(wav_data, wit_client)

                if text:
                    print(f"Transcription: {text}")
                else:
                    print("Could not transcribe audio.")

            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
            except KeyboardInterrupt:
                print("Stopping...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()