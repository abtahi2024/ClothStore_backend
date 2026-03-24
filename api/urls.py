from rest_framework.routers import DefaultRouter,SimpleRouter
from product.views import *
from order.views import *
from django.urls import *
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('categories',CategoryViewSet)
router.register('products',ProductViewSet,basename='products')
router.register('carts',CartViewSet,basename='carts')
router.register('orders',OrderViewSet,basename='orders')
router.register('wishlist',WishlistViewSet,basename='wishlist')

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',ReviewViewSet,basename='product-review')
product_router.register('images',ProductImageViewSet,basename='product_images')

cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')


urlpatterns= [
    path("", include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    # path('payment/',include('payments.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/',include('users.urls')),
    path('auth/social/', include('social_django.urls',namespace='social')),
    path('payment/initiale/',initiale_payment,name='initiate-payment'),
    path('payment/success/',payment_success,name='payment-success'),
    path('payment/cancel/',payment_cancel,name='payment-cancel'),
    path('payment/fail/',payment_fail,name='payment-fail'),
    path('orders/has-ordered/<int:product_id>/',HasOrderProduct.as_view())
]
