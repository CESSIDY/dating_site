from django import forms
from account_settings.models import Gallery
from django.forms import TextInput


class GalleryForm(forms.ModelForm):
    #tags = forms.CharField(required=False, type: 'hidden')

    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            #'user': TextInput(attrs={'type': 'hidden', 'required': False}),
            'tags': TextInput(attrs={'data-role': 'tagsinput', 'type': 'text'}),
        }
        exclude = ('user',)
