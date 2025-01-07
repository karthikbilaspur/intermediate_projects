
# Import necessary libraries
import speech_recognition as sr
import pyttsx3
from google.cloud import speech
from google.oauth2 import service_account
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize speech recognition
r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 4000

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Set up Google Speech Recognition credentials
credentials_path = 'path/to/your/service_account_key.json'
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Set up Google Speech Recognition client
client = speech.SpeechClient(credentials=credentials)

# Define speech recognition function
def recognize_speech(audio):
    """Perform speech recognition using Google Cloud Speech API."""
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

# Define listen function
def listen():
    """Listen to audio input from the microphone."""
    logging.info('Listening to audio input...')
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=5)
        audio_bytes = audio.get_wav_data()
        transcript = recognize_speech(audio_bytes)
        logging.info('Audio input processed.')
        return transcript

# Define speak function
def speak(text):
    """Speak the given text using the text-to-speech engine."""
    logging.info(f'Speaking text: {text}')
    engine.say(text)
    engine.runAndWait()

# Define main function
def main():
    logging.info('Starting main loop...')
    while True:
        transcript = listen()
        if transcript:
            logging.info(f'Transcript: {transcript}')
            speak(transcript)

# Run main function
if __name__ == "__main__":
    main()