from django.db import transaction
from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BookSerializer
from notifications.telegram import send_telegram_notification


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )
        read_only_fields = ("id", "actual_return_date", "user")


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "borrow_date")


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )
        read_only_fields = ("id", "actual_return_date", "user")


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book", "expected_return_date")

    def validate(self, attrs):
        book = attrs.get("book")
        if book.inventory <= 0:
            raise serializers.ValidationError(
                "This book is not available right now."
            )
        return attrs

    def create(self, validated_data):
        user_request = self.context.get("request")
        book = validated_data.get("book")
        with transaction.atomic():
            book.inventory -= 1
            book.save()
            borrowing = Borrowing.objects.create(
                user=user_request.user, book=book, **validated_data
            )

        message = (
            f"<b>NEW BORROWING</b>\n"
            f"User: {user_request.user.full_name} (ID: {user.id})\n"
            f"Book: {book.title} (ID: {book.id})"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        send_telegram_notification(message)

        return borrowing
