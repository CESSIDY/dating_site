from django.urls import path
from .views import (
    AboutMeView,
    GalleryList,
    AboutYouView,
    UserInfoView,
)

# app_name = 'account_show'
urlpatterns = [
    path('about_me', AboutMeView.as_view(), name='about_me'),
    path('about_you', AboutYouView.as_view(), name='about_you'),
    path('gallery', GalleryList.as_view(), name='gallery'),
    path('profile', UserInfoView.as_view(), name='user.profile'),
]
