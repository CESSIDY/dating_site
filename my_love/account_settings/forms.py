from django import forms
from django.contrib.contenttypes.models import ContentType
from .questionary.settings import form_answer_prefix as answer_prefix
from . import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import AboutYou, AboutMe, Question, Answer, Questionary
from django.forms import *
from taggit.forms import *
from django_select2 import forms as s2forms


class QuestionaryForm(forms.Form):
    object_id = forms.HiddenInput()
    question_id = forms.HiddenInput()
    answer = forms.RadioSelect()

    class Meta:
        fields = 'object_id, answer, question_id'

    def get_answer_field(self, question_obj, object):
        answers_list = []
        for answer in Answer.objects.filter(question=question_obj):
            answers_list.append((answer.pk, answer.title))

        answer_init = ''
        try:
            question = Questionary.objects.get(object_id=object.pk, question=question_obj.pk)
            if question:
                answer_init = question.answer.pk
        except:
            pass
        return forms.ChoiceField(
            initial=answer_init,
            widget=forms.RadioSelect, label=question_obj.title,
            choices=tuple(answers_list))


class AboutMeQuestionaryForm(QuestionaryForm):
    def __init__(self, user: '', question_obj: '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_id'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['question_id'].initial = question_obj.pk
        self.fields['{}{}'.format(answer_prefix, question_obj.pk)] = self.get_answer_field(question_obj, user.aboutme)

    def save(self, commit=True):
        instance = super(AboutMeQuestionaryForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class AboutYouQuestionaryForm(QuestionaryForm):
    def __init__(self, user: '', question_obj: '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_id'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['question_id'].initial = question_obj.pk
        self.fields['{}{}'.format(answer_prefix, question_obj.pk)] = self.get_answer_field(question_obj, user.aboutyou)

    def save(self, commit=True):
        instance = super(AboutYouQuestionaryForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


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
        # for field in iter(self.fields):
        #     self.fields[field].widget.attrs.update({
        #         # Change 'id' of input for easy use in javascript
        #         'id': 'id_edit_' + field
        #     })
    class Meta:
        model = AboutMe
        fields = '__all__'
        widgets = {
            'user': TextInput(
                attrs={'type': 'hidden', 'class': 'form-control valid', 'id': 'wizard-validation-material-user'}),
            'activate': CheckboxInput(attrs={'class': 'css-control-input'}),
            'birthday': TextInput(
                attrs={'type': 'date', 'class': 'form-control valid', 'id': 'wizard-validation-material-birthday'}),
            'color_aye': s2forms.Select2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-color_aye'}),
            'color_hair': s2forms.Select2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-color_hair'}),
            'genres': s2forms.HeavySelect2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-genres'},
                data_view='heavy_data.background.genres'),
            'music_types': s2forms.HeavySelect2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-music_types'},
                data_view='heavy_data.background.music_types'),
            'films': s2forms.HeavySelect2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-films'},
                data_view='heavy_data.background.films'),
            'books': s2forms.HeavySelect2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-books'},
                data_view='heavy_data.background.books'),
            'hobbies': s2forms.HeavySelect2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-hobbies'},
                data_view='heavy_data.background.hobbies'),
            'foods': s2forms.HeavySelect2MultipleWidget(
                attrs={'class': 'form-control', 'id': 'wizard-validation-material-foods'},
                data_view='heavy_data.background.foods'),
            'country': s2forms.HeavySelect2Widget(
                attrs={'class': 'form-control valid', 'id': 'wizard-validation-material-country'},
                data_view='heavy_data.background.countries'),
            'growth': TextInput(
                attrs={'type': 'number', 'class': 'form-control valid', 'id': 'wizard-validation-material-growth'}),
            'weight': TextInput(
                attrs={'type': 'number', 'class': 'form-control valid', 'id': 'wizard-validation-material-weight'}),
            'gender': Select(
                attrs={'class': 'form-control valid', 'id': 'wizard-validation-material-gender'}),
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
