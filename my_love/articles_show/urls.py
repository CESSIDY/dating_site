from django.urls import path, re_path
from .views import (
    ArticlesList,
)

# app_name = 'account_settings'
urlpatterns = [
    re_path(r'^(?P<tag>.*)$', ArticlesList.as_view(),  name='articles_show'),
]
