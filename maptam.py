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

# Set up Google Cloud credentials
MAPS_API_KEY = "AIzaSyDNRHZ0bLIfV-7-FJK3V0_O4i11de4-12A"  # Replace with your Google Maps API key
TTS_JSON_PATH = r"C:\\Users\\admin\\Desktop\\stt\\New folder\\text-to-speech-455413-09c4f83b2fbd.json"  # Replace with your actual path

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
            language_code="ta-IN", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
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
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print("கேட்கிறது...")
        beep()
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="ta-IN")
            return text
        except sr.UnknownValueError:
            speak("மன்னிக்கவும், நான் புரிந்துகொள்ளவில்லை. மீண்டும் முயற்சிக்கவும்.")
            return None
        except sr.RequestError:
            speak("நெட்வொர்க் பிழை. உங்கள் இணைய இணைப்பை சரிபார்க்கவும்.")
            return None

# Get directions from Google Maps API
def get_directions(destination):
    try:
        directions = gmaps.directions("Saveetha Engineering College, Chennai, Tamil Nadu", destination, mode="walking")
        if directions:
            return directions[0]['legs'][0]['steps']
        else:
            return None
    except Exception as e:
        print(f"Error fetching directions: {e}")
        return None

# Dictionary to translate directions to Tamil
direction_translations = {
    "Turn left": "இடதுபுறம் திரும்பவும்",
    "Turn right": "வலதுபுறம் திரும்பவும்",
    "Go straight": "நேராக செல்லவும்",
    "Head north": "வடக்கே செல்லவும்",
    "Head south": "தெற்கே செல்லவும்",
    "Head east": "கிழக்கே செல்லவும்",
    "Head west": "மேற்கே செல்லவும்",
    "Continue straight": "நேராக தொடர்ந்து செல்லவும்",
    "Take the exit": "வெளியேறும் பாதையை எடுக்கவும்",
    "Make a U-turn": "யு-டர்ன் எடுக்கவும்"
}

# Function to translate instructions
def translate_instruction(instruction):
    for eng, tam in direction_translations.items():
        instruction = instruction.replace(eng, tam)
    return instruction

# Navigate through the steps
def navigate(steps):
    if steps:
        for step in steps:
            instruction = step['html_instructions']
            instruction = instruction.replace("<b>", "").replace("</b>", "").replace("<div style=\"font-size:0.9em\">", "").replace("</div>", "")
            instruction = translate_instruction(instruction)  # Translate to Tamil
            distance = step['distance']['text']
            speak(f"{instruction}. தூரம்: {distance}")
            time.sleep(3)
        speak("நீங்கள் உங்கள் இலக்கை அடைந்துவிட்டீர்கள்.")

# Confirm input using keyboard key press
def confirm_input(input_text):
    speak(f"நீங்கள் கூறியது: {input_text}. உறுதி செய்ய Y அழுத்தவும் அல்லது மறுபடியும் முயற்சிக்க N அழுத்தவும்.")
    while True:
        if keyboard.is_pressed("y"):
            return True
        elif keyboard.is_pressed("n"):
            return False

# Main program loop
if __name__ == "__main__":
    speak("வணக்கம்! வழிகாட்டுதல் தொடங்க 1 அழுத்தவும்.")
    print("Press 1 to start navigation.")

    while True:
        if keyboard.is_pressed("1"):
            speak("நீங்கள் வழிகாட்டுதலைத் தொடங்க முடிவு செய்தீர்கள்.")
            break
        time.sleep(0.1)

    while True:
        destination = get_voice_input("உங்கள் இலக்கு இடத்தைக் கூறுங்கள்.")
        if destination:
            time.sleep(3)
            if confirm_input(destination):
                steps = get_directions(destination)
                if steps:
                    speak("வழிகாட்டுதல் தொடங்குகிறது.")
                    navigate(steps)
                break
            else:
                speak("இலக்கு தவறாக உள்ளது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.")