
# Assistive Navigation and Health Monitoring System (Tamil & English Voice Assistant)

This is a Python-based voice-controlled assistive application that helps blind, elderly, and differently-abled users with:
- Real-time **voice-based navigation** in Tamil or English.
- **Emergency SOS messaging** through WhatsApp (via Twilio) and Telegram.
- **Health monitoring** using sensors and voice feedback.

The app starts when you press the **spacebar**, then listens for the language choice (Tamil or English), and activates the appropriate module.

---

## Features

- Voice-controlled interface
- Real-time navigation using Google Maps
- Text-to-Speech feedback in Tamil/English
- SOS alert to family via WhatsApp and Telegram
- Health rate monitoring and alerts

---

## Requirements

- Python 3.8+
- Microphone for voice input
- Internet connection

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/assistive-system.git
cd assistive-system
```

2. Install required Python libraries:

```bash
pip install -r requirements.txt
```

---

## 🔑 How to Set Up API Keys

To use this app, you’ll need API credentials from Google Cloud, Twilio, and Telegram. Follow the steps below:

---

### 1. Google Cloud Text-to-Speech (TTS) API

#### Steps:
- Go to: https://console.cloud.google.com/
- Create a new project.
- Enable **Text-to-Speech API**.
- Go to **IAM & Admin > Service Accounts**.
- Create a service account and download the **JSON key file**.

#### Add to your environment:

Linux/macOS:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/your/service-account.json"
```

Windows (CMD):
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account.json
```

---

### 2. Google Maps API Key

#### Steps:
- In the same Google Cloud project, go to **API & Services > Credentials**.
- Create an API key.
- Enable these APIs:
  - **Maps JavaScript API**
  - **Geocoding API**

#### Add to `config.py`:

```python
GOOGLE_MAPS_API_KEY = 'your-google-maps-api-key'
```

---

### 3. Twilio (WhatsApp)

#### Steps:
- Go to: https://www.twilio.com/
- Create a free account.
- Get your **Account SID**, **Auth Token**, and register a WhatsApp-enabled number.
- Set up a verified recipient in your Twilio Sandbox for WhatsApp.

#### Add to `config.py`:

```python
TWILIO_ACCOUNT_SID = 'your-account-sid'
TWILIO_AUTH_TOKEN = 'your-auth-token'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio Sandbox number
RECIPIENT_WHATSAPP_NUMBER = 'whatsapp:+91xxxxxxxxxx'  # Verified user
```

---

### 4. Telegram Bot Token and Chat ID

#### Steps:
- Search for `@BotFather` in Telegram and create a new bot.
- Get the **bot token**.
- Use `@userinfobot` or a script to get your **chat ID**.

#### Add to `config.py`:

```python
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
TELEGRAM_CHAT_ID = 'your-telegram-chat-id'
```

---

## 🧠 Running the Application

Make sure your environment variables and `config.py` are set up, then run:

```bash
python app.py
```

Now press the **spacebar** to start the voice assistant. Say “Tamil” or “English” to continue.

---

## 🛠 File Structure

```
assistive-system/
│
├── navintamil.py            # Tamil navigation + TTS + SOS
├── navinenglish.py          # English navigation + TTS + SOS
├── healthrateeng.py         # Health monitoring (English)
├── config.py                # API keys and sensitive values
├── app.py                   # Main launcher script
├── requirements.txt
└── README.md
```

---

## 🔐 Security Note

Keep your `config.py` or `.env` file **out of version control**:
```bash
echo "config.py" >> .gitignore
```

---

