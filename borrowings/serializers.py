from django.template.context_processors import request
from rest_framework import serializers
from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

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
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(
            user=user_request.user, book=book, **validated_data
        )
        return borrowing
