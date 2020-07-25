from django import forms
from . import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import AboutYou, AboutMe
from django.forms import TextInput
from taggit.forms import *
from django_select2 import forms as s2forms
from .questions.questionary import get_original_questions, get_original_questions_keys


class AboutMeQuestionaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = get_original_questions()

        for key, context in questions.items():
            self.fields[key] = forms.ChoiceField(widget=forms.RadioSelect,
                                                 label=context['question_me'],
                                                 choices=context['answers'])

    class Meta:
        fields = get_original_questions_keys


class AboutYouQuestionaryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = get_original_questions()

        for key, context in questions.items():
            self.fields[key] = forms.ChoiceField(widget=forms.RadioSelect,
                                                 label=context['question_you'],
                                                 choices=context['answers'])

    class Meta:
        fields = get_original_questions_keys


class AboutYouForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                # Change 'id' of input for easy use in javascript
                'id': 'id_edit_' + field, 'class': 'form-control'
            })

    class Meta:
        model = AboutYou
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={'type': 'hidden'}),
            'birthday': TextInput(attrs={'type': 'date'}),
            'color_aye': s2forms.Select2MultipleWidget(),
            'color_hair': s2forms.Select2MultipleWidget(),
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.genres'),
            'music_types': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.music_types'),
            'films': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.films'),
            'books': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.books'),
            'hobbies': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.hobbies'),
            'foods': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.foods'),
            'countries': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.countries'),
        }


class AboutMeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                # Change 'id' of input for easy use in javascript
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
            'genres': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.genres'),
            'music_types': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.music_types'),
            'films': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.films'),
            'books': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.books'),
            'hobbies': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.hobbies'),
            'foods': s2forms.HeavySelect2MultipleWidget(data_view='heavy_data.background.foods'),
            'country': s2forms.HeavySelect2Widget(data_view='heavy_data.background.countries'),
        }
        # exclude = ('user',)


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )
        exclude = ('password',)
