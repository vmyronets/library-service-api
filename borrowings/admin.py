from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "user",
        "borrow_date",
        "expected_return_date",
        "is_active"
    )
    list_filter = ("book", "user")
    search_fields =("book__title", "is_active")
    ordering = ("-borrow_date",)
