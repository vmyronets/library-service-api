from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)
from borrowings.tasks import send_borrowing_notification_task
from payments.stripe_helper import create_stripe_session


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        queryset = self.queryset

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_active:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        # we store loans and link users
        borrowing = serializer.save(user=self.request.user)

        borrowing.book.inventory -= 1
        borrowing.book.save()

        # create stripe session
        create_stripe_session(borrowing, self.request)

        message = (
            f"**NEW BORROWING**\n"
            f"User: {borrowing.user.email}\n"
            f"Book: {borrowing.book.title}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        send_borrowing_notification_task.delay(message)

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        """Return borrowed book and decrease inventory."""
        borrowing = self.get_object()
        if not borrowing.is_active:
            return Response(
                {"error": "This borrowing is already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            borrowing.return_book()
            if borrowing.actual_return_date > borrowing.expected_return_date:
                pass

        return Response(
            {"status": "Book returned successfully."},
            status=status.HTTP_200_OK
        )
