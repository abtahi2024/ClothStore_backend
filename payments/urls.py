from django.urls import path
from payments.views import SSLCommerzInitView, SSLCommerzSuccessView

urlpatterns = [
    path('init/', SSLCommerzInitView.as_view()),
    path('success/', SSLCommerzSuccessView.as_view()),
]
