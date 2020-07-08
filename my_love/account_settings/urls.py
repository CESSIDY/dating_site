from django.urls import path
from .views import (
    AboutYouUpdate,
    AboutMeUpdate,
    heavy_data_about_me,
    ProfileUpdate
)

# app_name = 'account_settings'
urlpatterns = [
    path('about_me', AboutMeUpdate.as_view(), name='edit_about_me'),
    path('profile/edit', ProfileUpdate.as_view(), name='edit.profile'),
    path('about_you', AboutYouUpdate.as_view(), name='edit_about_you'),
    path('heavy_data_about_me/genres', heavy_data_about_me, {'model': 'genres'}, name='heavy_data.about_me.genres'),
    path('heavy_data_about_me/music_types', heavy_data_about_me, {'model': 'music_types'},
         name='heavy_data.about_me.music_types'),
    path('heavy_data_about_me/films', heavy_data_about_me, {'model': 'films'}, name='heavy_data.about_me.films'),
    path('heavy_data_about_me/books', heavy_data_about_me, {'model': 'books'}, name='heavy_data.about_me.books'),
    path('heavy_data_about_me/hobbies', heavy_data_about_me, {'model': 'hobbies'}, name='heavy_data.about_me.hobbies'),
    path('heavy_data_about_me/foods', heavy_data_about_me, {'model': 'foods'}, name='heavy_data.about_me.foods'),
    path('heavy_data_about_me/countries', heavy_data_about_me, {'model': 'countries'},
         name='heavy_data.about_me.countries'),
]
