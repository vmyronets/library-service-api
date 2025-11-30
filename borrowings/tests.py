from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from borrowings.models import Borrowing
from books.models import Book
from borrowings.serializers import BorrowingCreateSerializer


class BorrowingsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="test12345"
        )
        self.client.force_authenticate(user=self.user)
        self.book_in_inventory = Book.objects.create(
            title="Test Book", author="Test Author", inventory=10, daily_fee=10.00
        )
        self.book_out_of_inventory = Book.objects.create(
            title="Test Book 2", author="Test Author 2", inventory=0, daily_fee=20.00
        )
        self.borrow_date = timezone.now().date()
        self.actual_return_date = self.borrow_date + timezone.timedelta(days=7)

    def test_borrow_date_less_than_return_date(self):
        invalid_return_date = self.actual_return_date - timezone.timedelta(days=8)
        borrowing = Borrowing(
            borrow_date=self.borrow_date,
            expected_return_date=invalid_return_date,
            book=self.book_in_inventory,
            user=self.user,
        )
        with self.assertRaises(ValidationError):
            borrowing.clean()

    def test_validate_book_in_inventory(self):
        borrowing_data = {
            "borrow_date": self.borrow_date,
            "expected_return_date": self.actual_return_date,
            "book": self.book_out_of_inventory.id,
            "user": self.user.id,
        }
        serializer = BorrowingCreateSerializer(data=borrowing_data)

        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "This book is not available right now.", str(e.exception)
        )

    def test_borrowing_create(self):
        borrowing_data = {
            "borrow_date": self.borrow_date,
            "expected_return_date": self.actual_return_date,
            "book": self.book_in_inventory.id,
            "user": self.user.id,
        }
        serializer = BorrowingCreateSerializer(data=borrowing_data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save(user=self.user)
        self.assertEqual(borrowing.book, self.book_in_inventory)
        self.assertEqual(borrowing.user, self.user)

    def test_book_inventory_decrement(self):
        inventory_before_borrowing = self.book_in_inventory.inventory

        response = self.client.post(
            reverse("borrowings:borrowing-list"),
            {
                "book": self.book_in_inventory.id,
                "expected_return_date": self.actual_return_date,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book_in_inventory.refresh_from_db()
        self.assertEqual(
            self.book_in_inventory.inventory, inventory_before_borrowing - 1
        )
