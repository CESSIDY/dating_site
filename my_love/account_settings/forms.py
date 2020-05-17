from django import forms
from . import models
from .models import AboutYou, AboutMe, Gallery
from django.forms import TextInput
from taggit.forms import *
from django_select2 import forms as s2forms


class MyWidget(s2forms.ModelSelect2MultipleWidget):
    data_view = 'heavy_data_about_me'
    max_results = 25


class GalleryForm(forms.ModelForm):
    tags = TagField()
    tags.widget.attrs.update({'data-role': 'tagsinput'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'id_create_' + field, 'class': 'form-control'
            })

    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={'type': 'hidden', 'value': '1'}),
            #'tags': TextInput(attrs={'data-role': 'tagsinput', 'type': 'text'}),
        }
        #exclude = ('user',)


class AboutYouForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'id_edit_' + field, 'class': 'form-control'
            })

    class Meta:
        model = AboutYou
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={'type': 'hidden'}),
            'birthday': TextInput(attrs={'type': 'date'}),
            #'color_aye': forms.ChoiceField(required=False),
            #'color_hair': forms.ChoiceField(required=False),
            'color_aye': s2forms.Select2MultipleWidget(),
            'color_hair': s2forms.Select2MultipleWidget(),
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.genres'),
            'music_types': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.music_types'),
            'films': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.films'),
            'books': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.books'),
            'hobbies': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.hobbies'),
            'foods': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.foods'),
            'countries': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.countries'),
        }


class AboutMeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'id_edit_' + field, 'class': 'form-control'
            })

    class Meta:
        model = AboutMe
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={'type': 'hidden'}),
            'birthday': TextInput(attrs={'type': 'date'}),
            'color_aye': s2forms.Select2MultipleWidget(),
            'color_hair': s2forms.Select2MultipleWidget(),
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.genres'),
            'music_types': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.music_types'),
            'films': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.films'),
            'books': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.books'),
            'hobbies': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.hobbies'),
            'foods': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.about_me.foods'),
            'country': s2forms.Select2Widget,
        }
        # exclude = ('user',)
