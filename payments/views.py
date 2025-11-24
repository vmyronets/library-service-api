import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentDetailSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("borrowing")
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(borrowing__user=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer

    @action(methods=["GET"], detail=True, url_path="success")
    def payment_success(self, request, pk=None):
        """
        Сюди Stripe перенаправляє користувача після успішної оплати.
        Ми перевіряємо це і змінюємо статус платежу.
        """
        payment = self.get_object()
        session_id = payment.session_id

        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == "paid":
            payment.status = Payment.PaymentStatus.PAID
            payment.save()
            return Response(
                {"status": "Payment successful! Thank you."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"status": "Payment not confirmed yet."},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=["GET"], detail=True, url_path="cancel")
    def payment_cancel(self, request, pk=None):
        """If the user cancels the payment, we return a message to him."""
        return Response(
            {
                "message": "Payment was cancelled. "
                           "You can try again later within 24 hours."
            },
            status=status.HTTP_200_OK
        )
