from django.urls import path
from .views import (
    like
)

# app_name = 'account_settings'
urlpatterns = [
    path('make/<int:pk>', like, name='make_like'),
]
