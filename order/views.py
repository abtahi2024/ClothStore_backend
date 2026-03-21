from django.shortcuts import render
from order.serializers import *
from rest_framework.viewsets import *
from rest_framework.mixins import *
from order.models import *
from rest_framework.permissions import *
from rest_framework.decorators import action
from order.services import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ 
from django.conf import settings as Backend_setting
from django.http import HttpResponseRedirect

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class=CartSerializers
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)
    @swagger_auto_schema(
            operation_summary='User can Create a Order',
            request_body=CartSerializers,
            responses={
                200: CartSerializers,
                400:'Bad Request'
            }
        )
    def create(self, request, *args, **kwargs):
        existing_cart=Cart.objects.filter(user=request.user).first()
        if existing_cart:
            serializer=self.get_serializer(existing_cart)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary='user can see the his cart id'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='only Admin can edit and delete the cart',
            request_body=CartSerializers,
            responses={
                204: CartSerializers,
                400:'Bad request'
            }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemsSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))
    @swagger_auto_schema(
            operation_summary='User can see his item list'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='user can create his items',
            request_body=CartItemsSerializer,
            responses={
                201:CartItemsSerializer,
                400:'Samething was Wrong'
            }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='User can Delete his items',
            request_body=CartItemsSerializer,
            responses={
                204:CartItemsSerializer,
                400:'Samething was Wrong'
            }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
    
class OrderViewSet(ModelViewSet):
    http_method_names=['get','post','delete','patch','head','options']

    @swagger_auto_schema(
            operation_summary='Only user can Cancel the orders status'
    )
    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        order=self.get_object()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status': 'Order Canceled'})
    @swagger_auto_schema(
            operation_summary='Only Admin can Changes the order status'
    )
    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order=self.get_object()
        serializer=UpdateOrderSerializer(order,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        return Response({'status': f'Order status updated to {request.data['status']}'})


    def get_permissions(self):
        if self.action in ['update_status','destroy']:
            return [IsAdminUser()] 
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action=='cancel':
            return EmptySerializer
        if self.action=='create':
            return CreateOrderSerializer
        elif self.action=='update_status':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id,'user':self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()

        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
    
    @swagger_auto_schema(
            operation_summary='Retrive a list of Order'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='User can create his Order',
            request_body=CreateOrderSerializer,
            responses={
                201:OrderSerializer,
                400:openapi.Response("Bad Request")
            }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Oreder id to see that'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='only admin can edit the order '
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can delete the orders',
            request_body=OrderSerializer,
            responses={
                204:OrderSerializer,
                400:'Samething Was Wrong'
            }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
class WishlistViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    http_method_names=['get','post','delete']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Wishlist.objects.none()

        return Wishlist.objects.select_related('product').filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddWishlistSerializer
        return WishlistSerializers
    
    def get_serializer_context(self):
        return {'user': self.request.user}
    
    @swagger_auto_schema(
            operation_summary='Retrive a list of Wislist'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='User can save his product and wishlists',
            request_body=AddWishlistSerializer,
            responses={
                201:AddWishlistSerializer,
                400:'Bad Requset'
            }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='User can rejects his products',
            request_body=WishlistSerializers,
            responses={
                204:WishlistSerializers,
                500:'Samething Was wrong'
            }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
def initiale_payment(request):
    user=request.user
    amount=request.data.get('amount')
    order_id=request.data.get("orderId")
    num_items=request.data.get('numItems')

    settings = { 'store_id': 'phima68e538afdcefc', 'store_pass': 'phima68e538afdcefc@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f'txn_{order_id}'
    post_body['success_url'] = f"{Backend_setting.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{Backend_setting.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{Backend_setting.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f'{user.first_name} {user.last_name}'
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_items
    post_body['product_name'] = "E-commerce Products"
    post_body['product_category'] = "Cloth"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    if response.get('status')=='SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({'error':'Payment initiation failed'},status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def payment_success(request):
    order_id=request.data.get('tran_id').split('_')[1]
    order=Order.objects.get(id=order_id)
    order.status='Ready To Ship'
    order.save()
    return HttpResponseRedirect(f'{Backend_setting.FRONTEND_URL}/orders/')
@api_view(['POST'])
def payment_cancel(requrst):
    return HttpResponseRedirect(f"{Backend_setting.FRONTEND_URL}/orders/")
@api_view(['POST'])   
def payment_fail(requrst):
    return HttpResponseRedirect(f"{Backend_setting.FRONTEND_URL}/orders/")
    