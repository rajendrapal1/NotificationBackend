from django.conf import settings
from twilio.rest import Client


def send_whatsapp_message(phone_number, message):

    # Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN )

    # Make sure number has whatsapp prefix
    if not phone_number.startswith("whatsapp:"):
        phone_number = f"whatsapp:{phone_number}"

    # Send WhatsApp message
    message_response = client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        to=phone_number,
        body=message
    )

    print("Message SID:", message_response.sid)

    return message_response.sid
