from django.db import models
from django.conf import settings
from borrowings.models import Borrowing


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment for borrowing"
        FINE = "FINE", "Fine for overdue borrowing"

    status = models.CharField(
        max_length=7,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    type = models.CharField(
        max_length=7,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT
    )
    borrowing = models.OneToOneField(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=500)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    def __str__(self):
        return f"{self.type} - {self.status} for borrowing {self.borrowing.id}"
