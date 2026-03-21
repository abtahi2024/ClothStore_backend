from django.urls import path
from users.views import RegisterView, GoogleLoginSuccess,TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("google/", GoogleLoginSuccess.as_view(), name="google-login"),
    path('refresh/',TokenRefreshView.as_view(),name="token-refresh")
]
