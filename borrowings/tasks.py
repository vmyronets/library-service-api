from datetime import date
from borrowings.models import Borrowing
from notifications.telegram import send_telegram_notification


def check_overdue_borrowings():
    """Checks overdue loans and sends notifications."""
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=date.today(),
        actual_return_date__isnull=True,
        is_active=True
    ).select_related("book", "user")

    if not overdue_borrowings.exists():
        send_telegram_notification("👍 **No borrowings overdue today!**")
        return

    for borrowing in overdue_borrowings:
        message = (
            f"**BOOK OVERDUE!** (ID: {borrowing.id})\n"
            f"User: {borrowing.user.email} (ID: {borrowing.user.id})\n"
            f"Book: {borrowing.book.title}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        send_telegram_notification(message)
