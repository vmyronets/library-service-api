import requests

from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
CHAT_ID = settings.TELEGRAM_CHAT_ID
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram_notification(message: str):
    """Sends a message to the administrative chat in Telegram."""
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Telegram token or chat ID not configured.")
        return False

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        response.raise_for_status()
        return response.json().get("ok", False)
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram notification: {e}")

        return False
