from django.utils import timezone

from notifications.models import ( NotificationTemplate, NotificationLog,UserDevice)

from users.models import UserProfile

from .whatsapp import send_whatsapp_message
from .email_service import send_email_notification
from .web_push import send_web_push_message




def send_notification(user, subject, message):

    # Get phone number from UserProfile
    phone_number = "718515155"

    # try:
    #     phone_number = user.userprofile.phone_number
    # except UserProfile.DoesNotExist:
    #     print("UserProfile not found for:", user.username)

    # Email
    try:
        email_result = send_email_notification(  user, subject,message )
        print("Email result:", email_result)
    except Exception as e:
        print("Email error:", e)

    # WhatsApp
    try:
        if phone_number:
            send_whatsapp_message(
                phone_number,
                message
            )
        else:
            print("Phone number not found")
    except Exception as e:
        print("WhatsApp error:", e)

    # Web Push
    try:
        send_web_push_message(
            user,
            subject,
            message
        )
    except Exception as e:
        print("Web push error:", e)

    return True

