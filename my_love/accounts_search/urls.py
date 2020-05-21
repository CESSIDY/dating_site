from django.urls import include, path
from .views import (
    AccountDetailView,
    AccountsListView,
    partners_search,
)

# app_name = 'accounts_search'
urlpatterns = [
    path('', AccountsListView.as_view(), name='accounts_list'),
    path('partner_search', partners_search, name='partners_search'),
    path('<int:pk>', AccountDetailView.as_view(), name='account_show'),
]
