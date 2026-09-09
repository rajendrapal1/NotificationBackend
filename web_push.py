import requests
from decouple import config


ONESIGNAL_APP_ID = config(
    "ONESIGNAL_APP_ID",
    default=""
)

ONESIGNAL_REST_API_KEY = config(
    "ONESIGNAL_REST_API_KEY",
    default=""
)


def send_web_push_message(subscription_id, title, message):

    if not ONESIGNAL_APP_ID:
        return {
            "success": False,
            "error": "OneSignal App ID is missing."
        }

    if not ONESIGNAL_REST_API_KEY:
        return {
            "success": False,
            "error": "OneSignal REST API key is missing."
        }

    url = "https://api.onesignal.com/notifications"

    headers = {
        "Authorization": f"Key {ONESIGNAL_REST_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "app_id": ONESIGNAL_APP_ID,
        "include_subscription_ids": [
            subscription_id
        ],
        "headings": {
            "en": title
        },
        "contents": {
            "en": message
        }
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        response_data = response.json()

        if response.ok:
            return {
                "success": True,
                "response": response_data
            }

        return {
            "success": False,
            "response": response_data,
            "error": response.text
        }

    except requests.RequestException as e:

        return {
            "success": False,
            "error": str(e)
        }