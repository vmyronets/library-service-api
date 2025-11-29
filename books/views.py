from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """Only admin users can create, update or delete books."""
        if self.action in ("list", "retrieve"):
            return [IsAuthenticatedOrReadOnly()]

        return [IsAdminUser()]
