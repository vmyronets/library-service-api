from celery import shared_task
from django.utils import timezone
from borrowings.models import Borrowing
from notifications.telegram import send_telegram_notification


@shared_task
def send_borrowing_notification_task(message):
    """Asynchronous task for sending a message."""
    send_telegram_notification(message)


@shared_task
def check_overdue_borrowings():
    """Daily check of overdue books."""
    today = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=today,
        actual_return_date__isnull=True,
        is_active=True
    ).select_related("book", "user")

    if not overdue_borrowings.exists():
        send_telegram_notification("No borrowings overdue today!")
        return

    for borrowing in overdue_borrowings:
        message = (
            f"BOOK OVERDUE! (ID: {borrowing.id})\n"
            f"User: {borrowing.user.email} (ID:{borrowing.user.id})\n"
            f"Book: {borrowing.book.title}\n"
            f"Due date: {borrowing.expected_return_date}"
        )
        send_telegram_notification(message)
