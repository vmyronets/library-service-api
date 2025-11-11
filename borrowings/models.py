from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(default=timezone.now)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.expected_return_date <= self.borrow_date:
            raise ValidationError(
                "Expected return date must be after borrow date"
            )

    def return_book(self):
        if not self.is_active:
            raise ValidationError("This borrowing is already returned")
        self.actual_return_date = timezone.now().date()
        self.is_active = False
        self.book.inventory += 1
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.user} borrowed {self.book.title}"
