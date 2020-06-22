from django.urls import path
from .views import (
    ArticleDelete,
    ArticleCreate,
    ArticleUpdate,
)

# app_name = 'account_settings'
urlpatterns = [
    path('create', ArticleCreate.as_view(), name='create_article'),
    path('update/<pk>', ArticleUpdate.as_view(), name='update_article'),
    path('delete/<pk>', ArticleDelete.as_view(), name='delete_article'),
]
