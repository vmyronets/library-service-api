import stripe
from django.conf import settings
from django.urls import reverse
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(borrowing, request):
    """
    Creates a Stripe Session for borrowing and records Payment in the database.
    """
    # Calculation of the amount. We count the days.
    # Minimum 1 day, even if they take it and return it today.
    days_count = (borrowing.expected_return_date - borrowing.borrow_date).days
    if days_count <= 0:
        days_count = 1

    amount = int(days_count * borrowing.book.daily_fee * 100)

    payment = Payment.objects.create(
        status=Payment.PaymentStatus.PENDING,
        type=Payment.PaymentType.PAYMENT,
        borrowing=borrowing,
        user=borrowing.user,
        money_to_pay=amount / 100,  # We store in dollars in the database
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
                    "name": f"Borrowing: {borrowing.book.title}",
                },
                "unit_amount": amount,
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
