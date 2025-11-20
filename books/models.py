from django.db import models


class Book(models.Model):

    class BookCover(models.TextChoices):
        SOFT = "SOFT", "Soft cover"
        HARD = "HARD", "Hard cover"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=4,
        choices=BookCover.choices,
        default=BookCover.HARD
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title