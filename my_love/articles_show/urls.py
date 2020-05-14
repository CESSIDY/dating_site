from django.urls import path
from .views import (
    ArticlesList,
)

# app_name = 'account_settings'
urlpatterns = [
    path('', ArticlesList.as_view(), name='articles_show'),
]
