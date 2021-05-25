from django.urls import path

from authentication.views import CustomAuthToken

urlpatterns = [
    path('auth/obtain/', CustomAuthToken.as_view(), name="auth-token")
]
