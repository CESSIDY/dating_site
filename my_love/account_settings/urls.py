from django.urls import path
from .views import (
    AboutYouUpdate,
    AboutMeUpdate,
    ProfileUpdate,
    DataBaseAutoComplete,
)

# app_name = 'account_settings'
urlpatterns = [
    path('about_me', AboutMeUpdate.as_view(), name='edit_about_me'),
    path('profile/edit', ProfileUpdate.as_view(), name='edit.profile'),
    path('about_you', AboutYouUpdate.as_view(), name='edit_about_you'),
    path('data_base_auto_complete', DataBaseAutoComplete, name='data_base_auto_complete'),
]
