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
    }

    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        response.raise_for_status()
        return response.json().get("ok", False)
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram notification: {e}")

        return False


def get_borrow_time(obj):
    duration = obj.expected_return_date - obj.borrow_date
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    if hours > 0:
        return f"{hours} hours, {minutes} minutes"
    return f"{minutes} minutes"


def get_message(instance):
    user_name = instance.user.email
    book_title = instance.book.title
    book_author = instance.book.author
    borrowing_time = get_borrow_time(instance)
    message = (
        f"New borrowing:\n"
        f"User: {user_name}, Book: {book_title}, {book_author}\n"
        f"Borrow for: {borrowing_time}\n"
        f"Borrowing end: {instance.expected_return_date}"
    )
    return message
