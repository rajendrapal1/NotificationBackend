from django.conf import settings
from django.core.mail import send_mail


def send_email_notification(user, subject, message):

    print("User:", user.username)
    print("Sending email to:", settings.DEFAULT_FROM_EMAIL)

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    print("Email sent successfully")

    return True
