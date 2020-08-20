from django.urls import path
from .views import (
    newsGenerate
)

urlpatterns = [
    path('generate', newsGenerate, name='news'),
]