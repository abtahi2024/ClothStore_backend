from django.shortcuts import render
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payments.models import Payment
from order.models import Order
from django.shortcuts import get_object_or_404

class SSLCommerzInitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        # payment = Payment.objects.get(id=payment_id, user=request.user)
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        data = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
            'total_amount': payment.amount,
            'currency': 'BDT',
            'tran_id': f'TXN_{payment.id}',
            'success_url': settings.SSLCOMMERZ_SUCCESS_URL,
            'fail_url': settings.SSLCOMMERZ_FAIL_URL,
            'cancel_url': settings.SSLCOMMERZ_CANCEL_URL,

            'cus_name': request.user.email,
            'cus_email': request.user.email,
            'cus_phone': request.user.phone_number or '01700000000',
            'cus_add1': request.user.address or 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_country': 'Bangladesh',

            'shipping_method': 'NO',
            'product_name': 'Order Payment',
            'product_category': 'Ecommerce',
            'product_profile': 'general',
        }

        response = requests.post(
            settings.SSLCOMMERZ_INIT_URL,
            data=data
        )

        result = response.json()
        return Response({
            'payment_url': result.get('GatewayPageURL')
        })


class SSLCommerzSuccessView(APIView):
    permission_classes = []

    def post(self, request):

        tran_id = request.data.get("tran_id")or request.GET.get('tran_id')
        val_id = request.data.get("val_id")or request.GET.get('val_id')

        verify_url = f"https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"

        params = {
            "val_id": val_id,
            "store_id": settings.SSLCOMMERZ_STORE_ID,
            "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
            "format": "json"
        }

        response = requests.get(verify_url, params=params)
        result = response.json()

        if result.get("status") == "VALID":

            payment_id = tran_id.replace("TXN_", "")
            payment = Payment.objects.get(id=payment_id)

            payment.status = Payment.SUCCESS
            payment.transaction_id = tran_id
            payment.save()

            order = payment.oreder
            order.status = Order.READY_TO_SHIP
            order.save()

            return Response({"message": "Payment verified"})

        return Response({"message": "Payment failed"})
