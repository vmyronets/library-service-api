from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user", "expected_return_date")
    list_filter = ("book", "user")
    search_fields =("book__title", "user__is_active")
    ordering = ("-borrow_date",)
