from django.urls import include, path
from .views import (
    AccountDetailView,
    AccountsListView,
)

# app_name = 'accounts_search'
urlpatterns = [
    path('', AccountsListView.as_view(), name='accounts_list'),
    path('<int:pk>', AccountDetailView.as_view(), name='account_show'),
]
