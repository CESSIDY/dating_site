from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import *


class SignupCreate(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('home')
