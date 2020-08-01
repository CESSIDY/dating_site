from .models import Gallery
from django.forms import TextInput
from taggit.forms import *


class GalleryForm(forms.ModelForm):
    # Add for correct use tags widget
    tags = TagField()
    tags.widget.attrs.update({'data-role': 'tagsinput'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                # Change 'id' of input for easy use in javascript
                'id': 'id_create_' + field, 'class': 'form-control'
            })

    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            # Default value for user field to avoid mistakes
            #'user': TextInput(attrs={'type': 'hidden', 'value': '1'}),
            'pub_date': TextInput(attrs={'type': 'hidden'}),
            #'tags': TextInput(attrs={'data-role': 'tagsinput', 'type': 'text'}),
        }
        exclude = ('user',)

