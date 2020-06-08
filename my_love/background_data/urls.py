from django.urls import path
from .views import (
    upload_data,
)

# app_name = 'background_data'
urlpatterns = [
    path('accounts_data/genres', upload_data, {'model': 'genres'}, name='background.accounts_data.genres'),
    path('accounts_data/music_types', upload_data, {'model': 'music_types'}, name='background.accounts_data.music_types'),
    path('accounts_data/films', upload_data, {'model': 'films'}, name='background.accounts_data.films'),
    path('accounts_data/books', upload_data, {'model': 'books'}, name='background.accounts_data.books'),
    path('accounts_data/hobbies', upload_data, {'model': 'hobbies'}, name='background.accounts_data.hobbies'),
    path('accounts_data/foods', upload_data, {'model': 'foods'}, name='background.accounts_data.foods'),
    path('accounts_data/countries', upload_data, {'model': 'countries'}, name='background.accounts_data.countries'),
]
