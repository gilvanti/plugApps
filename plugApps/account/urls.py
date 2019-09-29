from django.urls import path, include
from account.views import RegistrationView, ConfirmRegistrationView

app_name = 'account'

urlpatterns = [
    path('registro/', RegistrationView.as_view(), name='registration'),
    path('confirm/', ConfirmRegistrationView.as_view(), name='confirm'),
]
