from django.contrib import admin
from django.db import transaction

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "book",
        "borrow_date",
        "expected_return_date",
        "is_active",
    )
    list_filter = ("is_active", "book", "user")
    search_fields = ("user__email", "book__title")

    def save_model(self, request, obj, form, change):
        """
        This method is called when the administrator clicks 'Save'.
        change = True if it is an edit.
        change = False if it is a new creation.
        """
        with transaction.atomic():
            # If it is CREATION (not editing)
            if not change:
                obj.book.inventory -= 1
                obj.book.save()

            # Call up standard saving Borrowing
            super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        This method is called when the admin deletes a record.
        """
        with transaction.atomic():
            obj.book.inventory += 1
            obj.book.save()
            super().delete_model(request, obj)
