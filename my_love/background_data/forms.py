from django import forms
from . import models
from django.forms import TextInput
from django_select2 import forms as s2forms


class GenresForm(forms.ModelForm):
    class Meta:
        model = models.Genres
        fields = '__all__'


class FoodsForm(forms.ModelForm):
    class Meta:
        model = models.Foods
        fields = '__all__'


class CountriesForm(forms.ModelForm):
    class Meta:
        model = models.Countries
        fields = '__all__'


class FilmsForm(forms.ModelForm):
    class Meta:
        model = models.Films
        fields = '__all__'
        widgets = {
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.genres'),
        }


class BooksForm(forms.ModelForm):
    class Meta:
        model = models.Books
        fields = '__all__'
        widgets = {
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.genres'),
        }


class HobbiesForm(forms.ModelForm):
    class Meta:
        model = models.Hobbies
        fields = '__all__'


class MusicTypesForm(forms.ModelForm):
    class Meta:
        model = models.MusicType
        fields = '__all__'
        widgets = {
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.genres'),
        }

