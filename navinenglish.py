import os
import time
import tempfile
import keyboard
import io
import requests
from twilio.rest import Client
from google.cloud import texttospeech
import pygame
import speech_recognition as sr
import googlemaps
import winsound
from bs4 import BeautifulSoup

# --- Configuration ---
GOOGLE_TTS_JSON = r"C:\\Users\\admin\\Desktop\\stt\\project2\\text-to-speech-455413-09c4f83b2fbd.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_JSON

MAPS_API_KEY = "AIzaSyDNRHZ0bLIfV-7-FJK3V0_O4i11de4-12A"
gmaps = googlemaps.Client(key=MAPS_API_KEY)

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
EMERGENCY_CONTACT = "whatsapp:+91XXXXXXXXXX"

latitude = "12.9715987"
longitude = "77.5945627"
location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

pygame.init()
pygame.mixer.init()

# --- Text-to-Speech ---
def speak(text):
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-IN", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(response.audio_content)
            tmp_path = tmp.name

        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if keyboard.is_pressed("0"):
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                os.remove(tmp_path)
                speak("Returning to the main menu.")
                raise KeyboardInterrupt
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove(tmp_path)

    except Exception as e:
        print(f"TTS Error: {e}")
        print(text)

def beep():
    winsound.Beep(1000, 200)

def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    speak(prompt)
    beep()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            text = recognizer.recognize_google(audio, language="en-IN")
            print("🗣️ You said:", text)
            return text
    except sr.WaitTimeoutError:
        speak("Could not hear you. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please repeat.")
    except sr.RequestError as e:
        speak("Internet issue. Please try again.")
        print("API Error:", e)
    except Exception as e:
        speak("Microphone error occurred.")
        print("Microphone Error:", e)

    return None

def check_for_main_menu():
    if keyboard.is_pressed("0"):
        speak("Main Menu: Press 1 for Navigation, 2 for SOS, or 0 to Exit.")
        return True
    return False

def get_directions(destination):
    try:
        directions = gmaps.directions("Saveetha Engineering College", destination, mode="walking")
        return directions[0]['legs'][0]['steps'] if directions else None
    except Exception as e:
        print("Error:", e)
        return None

def clean_html_instruction(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()

def start_navigation():
    while True:
        destination = get_voice_input("Please say your destination.")
        if destination:
            speak(f"You said: {destination}. Press 1 to confirm or 2 to re-enter.")
            while True:
                if check_for_main_menu():
                    return
                if keyboard.is_pressed("1"):
                    steps = get_directions(destination)
                    if steps:
                        for step in steps:
                            if check_for_main_menu():
                                return
                            instr_raw = step['html_instructions']
                            instr = clean_html_instruction(instr_raw)
                            speak(instr)
                            time.sleep(2)
                        speak("You have reached your destination.")
                    return
                elif keyboard.is_pressed("2"):
                    speak("Please say the destination again.")
                    break
                time.sleep(0.1)

def send_sos(button):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    if button == 1:
        msg = "🚨 POLICE CALL 🚨"
        number = "100"
    elif button == 2:
        msg = "🚑 AMBULANCE CALL 🚑"
        number = "108"
    elif button == 3:
        msg = "🔥 FIRE DEPT CALL 🔥"
        number = "101"
    else:
        msg = "❌ UNKNOWN EMERGENCY ❌"
        number = "N/A"

    body = f"{msg}\nHelp Needed!\n📍 Location: {location_link}\n📞 Emergency Number: {number}"
    client.messages.create(body=body, from_=TWILIO_WHATSAPP_NUMBER, to=EMERGENCY_CONTACT)
    speak(f"{msg} message has been sent.")

def sos_menu():
    speak("SOS Activated. Press 1 for Police, 2 for Ambulance, 3 for Fire Department, or 0 to go back.")
    while True:
        if check_for_main_menu():
            return
        if keyboard.is_pressed("1"):
            send_sos(1)
            time.sleep(1)
        elif keyboard.is_pressed("2"):
            send_sos(2)
            time.sleep(1)
        elif keyboard.is_pressed("3"):
            send_sos(3)
            time.sleep(1)
        time.sleep(0.1)

def main_menu():
    speak("Welcome! Press 1 for Navigation, 2 for SOS, or 0 to Exit.")
    while True:
        if keyboard.is_pressed("1"):
            speak("Starting navigation.")
            start_navigation()
        elif keyboard.is_pressed("2"):
            speak("Activating SOS.")
            sos_menu()
        elif keyboard.is_pressed("0"):
            speak("Thank you. Exiting.")
            exit()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        speak("Thank you. Application closed.")
        exit()
