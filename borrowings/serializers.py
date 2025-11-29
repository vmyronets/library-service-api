from rest_framework import serializers
from datetime import date

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
        read_only_fields = ("id", "actual_return_date", "user")


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "borrow_date")


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
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
                {"book": "This book is not available right now."}
            )

        expected_return_date = attrs.get("expected_return_date")

        if expected_return_date and expected_return_date <= date.today():
            raise serializers.ValidationError(
                {"expected_return_date": "Return date must be in the future."}
            )

        return attrs
