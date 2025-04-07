from twilio.rest import Client

# Twilio Account Details
TWILIO_SID = "ACb4fb756c1c4c5ccd0329ce491249379d"
TWILIO_AUTH_TOKEN = "2995cd7cec404f455524193d0dbf64b6"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio WhatsApp sandbox number
EMERGENCY_CONTACT = "whatsapp:+917338995840"  # Your emergency contact's WhatsApp number

# Your location (Replace with GPS data if needed)
latitude = "12.9715987"
longitude = "77.5945627"
location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

def send_sos_message(button_press_count):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    if button_press_count == 1:
        emergency_type = "🚨 CALLING POLICE 🚨"
        emergency_number = "100"  # Police emergency number
    elif button_press_count == 2:
        emergency_type = "🚑 CALLING AMBULANCE 🚑"
        emergency_number = "108"  # Ambulance emergency number
    elif button_press_count == 3:
        emergency_type = "🔥 CALLING FIRE DEPARTMENT 🔥"
        emergency_number = "101"  # Fire department emergency number
    else:
        emergency_type = "❌ UNKNOWN EMERGENCY ❌"
        emergency_number = "N/A"

    # WhatsApp Message Content
    message_body = f"{emergency_type}\nI NEED HELP!\n📍 Location: {location_link}\n📞 Emergency Number: {emergency_number}"

    # Send WhatsApp Message
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=EMERGENCY_CONTACT
    )

    print(f"SOS Message Sent! Message SID: {message.sid}")

# Example Usage (1 press = police, 2 press = ambulance, 3 press = fire)
send_sos_message(1)  # Simulates pressing the button once
