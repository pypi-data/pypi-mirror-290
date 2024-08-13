from django.urls import path

from .views import make_payment, success, verify

urlpatterns = [
    path('pay/', make_payment, name='make_payment'),
    path('verify/', verify, name='verify'),
    path('success/', success, name='success'),
]