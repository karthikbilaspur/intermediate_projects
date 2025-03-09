import speech_recognition as sr
import pyttsx3
from google.cloud import speech
from google.oauth2 import service_account
import logging
import os
import environ
import threading
import datetime
import pytz

# Project Name
PROJECT_NAME = "KarthikSpeech"

# Load environment variables
env = environ.Env()
env.read_env()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - {PROJECT_NAME} - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize speech recognition
r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = env.int('ENERGY_THRESHOLD', default=4000)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', env.int('SPEECH_RATE', default=150))

# Set up Google Speech Recognition credentials
credentials_path = env('GOOGLE_CREDENTIALS_PATH')
if not credentials_path:
    logging.error('Google credentials path not set')
    exit(1)

credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Set up Google Speech Recognition client
client = speech.SpeechClient(credentials=credentials)

# Define speech recognition function
def recognize_speech(audio):
    try:
        logging.info('Performing speech recognition...')
        encoding = speech.types.RecognitionConfig.AudioEncoding.LINEAR16
        config = speech.types.RecognitionConfig(encoding=encoding)
        audio_instance = speech.types.RecognitionAudio(content=audio)
        response = client.recognize(config, audio_instance)
        transcript = ''
        for result in response.results:
            transcript += result.alternatives[0].transcript
        logging.info('Speech recognition complete.')
        return transcript
    except Exception as e:
        logging.error(f'Speech recognition failed: {str(e)}')
        return ''

# Define listen function
def listen():
    try:
        logging.info('Listening to audio input...')
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=env.int('PHRASE_TIME_LIMIT', default=5))
            audio_bytes = audio.get_wav_data()
            return audio_bytes
    except Exception as e:
        logging.error(f'Audio input failed: {str(e)}')
        return None

# Define speak function
def speak(text):
    try:
        logging.info(f'Speaking text: {text}')
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f'Text-to-speech failed: {str(e)}')

# Define main function
def main():
    logging.info(f'Starting {PROJECT_NAME}...')
    speak(f'Welcome to {PROJECT_NAME}!')
    while True:
        try:
            audio_bytes = listen()
            if audio_bytes:
                transcript = recognize_speech(audio_bytes)
                logging.info(f'Transcript: {transcript}')
                threading.Thread(target=speak, args=(transcript,)).start()
                
                # Perform actions based on transcript
                if 'hello' in transcript.lower():
                    speak('Hello! How can I assist you today?')
                elif 'what is your name' in transcript.lower():
                    speak(f'My name is {PROJECT_NAME}.')
                elif 'what is the time' in transcript.lower():
                    current_time = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%I:%M %p')
                    speak(f'The current time is {current_time}.')
                elif 'exit' in transcript.lower():
                    speak(f'Exiting {PROJECT_NAME}. Goodbye!')
                    break
        except KeyboardInterrupt:
            logging.info(f'Stopping {PROJECT_NAME}...')
            break
        except Exception as e:
            logging.error(f'{PROJECT_NAME} failed: {str(e)}')

# Run main function
if __name__ == "__main__":
    main()