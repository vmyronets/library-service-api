from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer


class UnauthenticatedBooksAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list_auth_not_required(self):
        response = self.client.get(reverse("books:book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_detail_auth_required(self):
        response = self.client.get(
            reverse("books:book-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthenticatedBooksAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_book_list(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=10,
            daily_fee=10.00
        )
        response = self.client.get(reverse("books:book-list"))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_book_detail(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=10,
            daily_fee=10.00
        )
        response = self.client.get(
            reverse("books:book-detail", kwargs={"pk": book.id})
        )
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data[0])

    def test_book_delete_auth_required(self):
        response = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_create_admin_required(self):
        response = self.client.post(reverse("books:book-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_update_admin_required(self):
        response = self.client.put(
            reverse("books:book-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBooksAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="test12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book_admin_only(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "inventory": 10,
            "daily_fee": 10.00
        }
        response = self.client.post(reverse("books:book-list"), data=book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



