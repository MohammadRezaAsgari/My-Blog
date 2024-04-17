from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('sign-up/', UserCreateView.as_view(), name='sign-up'),
]