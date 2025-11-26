from django.db import models


class Book(models.Model):
    class BookCover(models.TextChoices):
        SOFT = "SOFT", "Soft cover"
        HARD = "HARD", "Hard cover"

    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=4,
        choices=BookCover.choices,
        default=BookCover.HARD
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.50
    )

    def __str__(self):
        return f"{self.title} by {self.author} - {self.daily_fee}"
