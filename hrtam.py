import requests
import time
import os
import random
import tempfile
from google.cloud import texttospeech
from playsound import playsound

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text-to-speech-455413-09c4f83b2fbd.json"

# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "7722919054:AAFYKU9dSpg-i_xTBpFJk66qzHdwV0Hd8f0"
TELEGRAM_CHAT_ID = "6338596536"

# Function to get mock health data
def get_health_data():
    return {
        "heart_rate": random.randint(50, 130),  
        "temperature": round(random.uniform(35.5, 39.0), 1),  
        "pulse": random.randint(50, 120)  
    }

# Function to send Telegram alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.get(url, params=params)

# Function to speak alert in Tamil using Google Cloud TTS
def speak_alert(message):
    client = texttospeech.TextToSpeechClient()

    # Set voice parameters (Tamil language)
    synthesis_input = texttospeech.SynthesisInput(text=message)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ta-IN", 
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Generate the speech
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save to a temp file and play
    temp_dir = tempfile.gettempdir()
    temp_audio_path = os.path.join(temp_dir, "alert_audio.mp3")

    with open(temp_audio_path, "wb") as out:
        out.write(response.audio_content)

    playsound(temp_audio_path)  
    os.remove(temp_audio_path)  

# Monitor health data every 10 seconds
while True:
    health_data = get_health_data()
    
    heart_rate = health_data["heart_rate"]
    temperature = health_data["temperature"]
    pulse = health_data["pulse"]

    print(f"💓 Heart Rate: {heart_rate} BPM | 🌡️ Temperature: {temperature}°C | 🔄 Pulse: {pulse} BPM")

    alerts = []
    if heart_rate < 55 or heart_rate > 120:
        alerts.append(f"⚠️ Heart Rate is abnormal: {heart_rate} BPM")
    if temperature < 36.0 or temperature > 38.0:
        alerts.append(f"⚠️ Temperature is abnormal: {temperature}°C")
    if pulse < 55 or pulse > 110:
        alerts.append(f"⚠️ Pulse Rate is abnormal: {pulse} BPM")

    if alerts:
        alert_message = "\n".join(alerts)
        print("🚨 ALERT:", alert_message)

        # Send alert to Telegram
        send_telegram_alert(alert_message)

        # Convert to Tamil for voice alert
        tamil_voice_message = "கவனி! உங்கள் உடல்நிலை அபாயகரமாக உள்ளது. " + " ".join(alerts)
        speak_alert(tamil_voice_message)

    time.sleep(10)  # Wait 10 seconds before fetching new data
