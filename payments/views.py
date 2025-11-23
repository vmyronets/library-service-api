import stripe

from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentDetailSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(borrowing__user=user)

    @action(
        methods=["GET"],
        detail=True,
        url_path="session-checkout",
        permission_classes=[IsAuthenticated]
    )
    def session_checkout(self, request, pk=None):
        domain_url = "http://localhost:8000/api/v1/payments/"
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + str(pk) + "/success/",
            cancel_url=domain_url + str(pk) + "/cancel/",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Borrowing",
                        },
                        "unit_amount": 1000,
                    },
                    "quantity": 1,
                }
            ]
        )
        return JsonResponse(
            {
                "sessionId": checkout_session.id,
                "sessionUrl": checkout_session.url
            },

        )
