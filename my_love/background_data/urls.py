from django.urls import path
from .views import (
    store_data,
    get_data_by_json,
)

# app_name = 'background_data'
urlpatterns = [
    path('accounts_data/genres', store_data, {'model': 'genres'}, name='background.accounts_data.genres'),
    path('accounts_data/music_types', store_data, {'model': 'music_types'}, name='background.accounts_data.music_types'),
    path('accounts_data/films', store_data, {'model': 'films'}, name='background.accounts_data.films'),
    path('accounts_data/books', store_data, {'model': 'books'}, name='background.accounts_data.books'),
    path('accounts_data/hobbies', store_data, {'model': 'hobbies'}, name='background.accounts_data.hobbies'),
    path('accounts_data/foods', store_data, {'model': 'foods'}, name='background.accounts_data.foods'),
    path('accounts_data/countries', store_data, {'model': 'countries'}, name='background.accounts_data.countries'),
    path('heavy_background_data/genres', get_data_by_json, {'model': 'genres'},
         name='heavy_data.background.genres'),
    path('heavy_background_data/music_types', get_data_by_json, {'model': 'music_types'},
         name='heavy_data.background.music_types'),
    path('heavy_background_data/films', get_data_by_json, {'model': 'films'},
         name='heavy_data.background.films'),
    path('heavy_background_data/books', get_data_by_json, {'model': 'books'},
         name='heavy_data.background.books'),
    path('heavy_background_data/hobbies', get_data_by_json, {'model': 'hobbies'},
         name='heavy_data.background.hobbies'),
    path('heavy_background_data/foods', get_data_by_json, {'model': 'foods'},
         name='heavy_data.background.foods'),
    path('heavy_background_data/countries', get_data_by_json, {'model': 'countries'},
         name='heavy_data.background.countries'),
]
