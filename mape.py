import os
import speech_recognition as sr
import googlemaps
import time
from gtts import gTTS
import io
import pygame
import keyboard
import winsound
from google.cloud import texttospeech
from google.oauth2 import service_account

# Set up Google Cloud credentials (Replace with your correct paths)
MAPS_API_KEY = "AIzaSyDNRHZ0bLIfV-7-FJK3V0_O4i11de4-12A"  # Replace with your Google Maps API key
TTS_JSON_PATH = r"C:\\Users\\admin\\Desktop\\stt\\New folder\\text-to-speech-455413-09c4f83b2fbd.json"   # Replace with your Google Cloud TTS JSON key file path

# Initialize Google Maps client
gmaps = googlemaps.Client(key=MAPS_API_KEY)

# Initialize pygame for TTS
pygame.init()
pygame.mixer.init()

# Beep sound function
def beep():
    frequency = 1000  # Hz
    duration = 200  # milliseconds
    winsound.Beep(frequency, duration)

# Text-to-Speech function using Google Cloud TTS
def speak(text):
    """Converts text to speech using Google Cloud Text-to-Speech."""
    try:
        credentials = service_account.Credentials.from_service_account_file(TTS_JSON_PATH)
        client = texttospeech.TextToSpeechClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(
            request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
        )

        audio_stream = io.BytesIO(response.audio_content)
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"TTS Error: {e}")
        print(text)

# Voice input function
def get_voice_input(prompt):
    """Captures voice input for the destination."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print("Listening...")
        beep()
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en-US")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please try again.")
            return None
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return None

# Get directions from Google Maps API
def get_directions(destination):
    """Fetches walking directions from Google Maps API."""
    try:
        directions = gmaps.directions("Saveetha Engineering College, Chennai, Tamil Nadu", destination, mode="walking")
        if directions:
            steps = directions[0]['legs'][0]['steps']
            return steps
        else:
            return None
    except Exception as e:
        print(f"Error fetching directions: {e}")
        return None

# Navigate through the steps
def navigate(steps):
    """Navigates through the steps."""
    if steps:
        for step in steps:
            instruction = step['html_instructions'].replace("<b>", "").replace("</b>", "").replace("<div style=\"font-size:0.9em\">", "").replace("</div>", "")
            distance = step['distance']['text']
            speak(f"{instruction}. Distance: {distance}")
            time.sleep(3)
        speak("You have reached your destination.")

# Confirm input using keyboard key press
def confirm_input(input_text):
    """Confirm the input using Y/N key press."""
    speak(f"You said: {input_text}. Press Y to confirm or N to retry.")
    while True:
        if keyboard.is_pressed("y"):
            return True
        elif keyboard.is_pressed("n"):
            return False

# Main program loop
if __name__ == "__main__":
    speak("Hello! Press 1 to start navigation.")
    print("Press 1 to start navigation.")

    while True:
        if keyboard.is_pressed("1"):
            speak("You have decided to start navigation.")
            break
        time.sleep(0.1)

    while True:
        destination = get_voice_input("Please say your destination.")
        if destination:
            time.sleep(3)

            if confirm_input(destination):
                steps = get_directions(destination)
                if steps:
                    speak("Starting navigation.")
                    navigate(steps)
                break
            else:
                speak("Invalid destination. Please try again.")
