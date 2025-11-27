import stripe
from django.conf import settings
from django.urls import reverse
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(
        borrowing,
        request,
        payment_type=Payment.PaymentType.PAYMENT,
        overdue_days=0
):
    """
    Creates a Stripe Session for borrowing and records Payment in the database.
    Allows as usual payment as well as overdue payment.
    """
    book = borrowing.book
    daily_fee = book.daily_fee

    if payment_type == Payment.PaymentType.FINE:
        amount = daily_fee * overdue_days * settings.FINE_MULTIPLIER
        product_name = f"Overdue Fine: {book.title} ({overdue_days} days)"
    else:
        days_count = (borrowing.expected_return_date - borrowing.borrow_date).days
        if days_count <= 0:
            days_count = 1
        amount = daily_fee * days_count
        product_name = f"Borrowing: {book.title}"

    unit_amount_cents = int(amount * 100)

    payment = Payment.objects.create(
        status=Payment.PaymentStatus.PENDING,
        type=payment_type,
        borrowing=borrowing,
        user=borrowing.user,
        money_to_pay=amount,  # We store in dollars in the database
        session_url="",
        session_id=""
    )

    success_url = request.build_absolute_uri(
        reverse("payments:payment-payment-success", args=[payment.id])
    )
    cancel_url = request.build_absolute_uri(
        reverse("payments:payment-payment-cancel", args=[payment.id])
    )

    # Creating a Stripe session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product_name,
                },
                "unit_amount": unit_amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
    )

    # Payment update
    payment.session_id = session.id
    payment.session_url = session.url
    payment.save()

    return payment
