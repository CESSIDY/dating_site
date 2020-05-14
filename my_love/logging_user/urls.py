from django.urls import include, path
from .views import (
    SignupCreate,
)

# app_name = 'logging_user'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', SignupCreate.as_view(), name='signup'),
]
