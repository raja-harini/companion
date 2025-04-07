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

# --- Configurations ---
GOOGLE_TTS_JSON = r"C:\\Users\\admin\\Desktop\\stt\\project2\\text-to-speech-455413-09c4f83b2fbd.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_JSON

# Google Maps API
MAPS_API_KEY = "AIzaSyDNRHZ0bLIfV-7-FJK3V0_O4i11de4-12A"
gmaps = googlemaps.Client(key=MAPS_API_KEY)

# Telegram
TELEGRAM_BOT_TOKEN = "7722919054:AAFYKU9dSpg-i_xTBpFJk66fHdwV0Hd8f0"
TELEGRAM_CHAT_ID = "6338596536"

# Twilio
TWILIO_SID = "ACb4fb756c1c4c5ccd0329ce491249379d"
TWILIO_AUTH_TOKEN = "2995cd7cec404f455524193d0dbf64b6"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
EMERGENCY_CONTACT = "whatsapp:+917338995840"

# Location
latitude = "12.9715987"
longitude = "77.5945627"
location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

# Setup pygame
pygame.init()
pygame.mixer.init()

# --- TTS Function ---
def speak(text):
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="ta-IN", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
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
                speak("முதன்மை மெனுவுக்கு திரும்புகிறோம்.")
                raise KeyboardInterrupt
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove(tmp_path)

    except Exception as e:
        print(f"TTS Error: {e}")
        print(text)

# --- Beep ---
def beep():
    winsound.Beep(1000, 200)

# --- Voice input ---
def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    speak(prompt)
    beep()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                print("🎤 Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                text = recognizer.recognize_google(audio, language="ta-IN")
                print("🗣️ You said:", text)
                return text
            except sr.WaitTimeoutError:
                speak("கேட்க இயலவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.")
            except sr.UnknownValueError:
                speak("புரியவில்லை. மீண்டும் கூறவும்.")
            except sr.RequestError as e:
                speak("இணைய பிரச்சனை. மீண்டும் முயற்சிக்கவும்.")
                print("API Error:", e)
    except Exception as e:
        speak("மைக்ரோஃபோனில் பிழை ஏற்பட்டது.")
        print("Microphone Error:", e)

    return None

# --- Check for main menu key ---
def check_for_main_menu():
    if keyboard.is_pressed("0"):
        speak("முதன்மை மெனு: 1 அழுத்தி வழிகாட்டல் தொடங்கவும், 2 அழுத்தி SOS செயல்படுத்தவும், 0 அழுத்தி வெளியேறவும்.")
        return True
    return False

# --- Navigation ---
def get_directions(destination):
    try:
        directions = gmaps.directions("Saveetha Engineering College", destination, mode="walking")
        return directions[0]['legs'][0]['steps'] if directions else None
    except Exception as e:
        print("Error:", e)
        return None

translations = {
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

def clean_html_instruction(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()

def translate_instruction(text):
    for eng, tam in translations.items():
        text = text.replace(eng, tam)
    return text

def start_navigation():
    while True:
        destination = get_voice_input("உங்கள் இலக்கை கூறுங்கள்.")
        if destination:
            speak(f"நீங்கள் கூறிய இடம்: {destination}. சரியா? சரியானால் 1 அழுத்தவும், தவறானால் 2 அழுத்தவும்.")
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
                            instr = translate_instruction(instr)
                            speak(instr)
                            time.sleep(2)
                        speak("நீங்கள் இலக்கை அடைந்துவிட்டீர்கள்.")
                    return
                elif keyboard.is_pressed("2"):
                    speak("மீண்டும் இடத்தை கூறுங்கள்.")
                    break
                time.sleep(0.1)

# --- SOS Message ---
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
    speak(f"{msg} குறுஞ்செய்தி அனுப்பப்பட்டுள்ளது.")

# --- SOS Menu ---
def sos_menu():
    speak("SOS செயல்படுத்தப்பட்டது.உதவிக்காக 1 போலீசுக்கு, 2 ஆம்புலன்ஸுக்கு, 3 தீயணைப்பு படைக்கு அழுத்தவும்,முதன்மை மெனுவுக்கு திரும்ப 0 அழுத்தவும்.")
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

# --- Main Program ---
def main_menu():
    speak("வணக்கம்! 1 அழுத்தி வழிகாட்டல் தொடங்கவும், 2 அழுத்தி SOS செயல்படுத்தவும், 0 அழுத்தி வெளியேறவும்.")
    while True:
        if keyboard.is_pressed("1"):
            speak("வழிகாட்டுதல் தொடங்குகிறது.")
            start_navigation()
        elif keyboard.is_pressed("2"):
            speak("SOS செயல்படுத்தப்படுகிறது.")
            sos_menu()
        elif keyboard.is_pressed("0"):
            speak("நன்றி. வெளியேறுகிறீர்கள்.")
            exit()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        speak("நன்றி. நீங்கள் செயலியை நிறுத்திவிட்டீர்கள்.")
        exit()
