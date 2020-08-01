from django.urls import path
from .views import (
    AboutYouUpdate,
    AboutMeUpdate,
    ProfileUpdate,
    AboutMeQuestionary,
)

# app_name = 'account_settings'
urlpatterns = [
    path('about_me', AboutMeUpdate.as_view(), name='edit_about_me'),
    path('about_me_questionary', AboutMeQuestionary.as_view(), name='edit_about_me_questionary'),
    path('profile/edit', ProfileUpdate.as_view(), name='edit.profile'),
    path('about_you', AboutYouUpdate.as_view(), name='edit_about_you'),
]
