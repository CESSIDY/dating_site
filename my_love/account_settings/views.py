from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import AboutMe, AboutYou
from background_data.models import Genres, MusicType, Films, Foods, Countries, Books, Hobbies
from .forms import *
import json
from django.http import HttpResponse
from django.views.generic import (
    UpdateView, FormView,
)


# update of (AboutYou Model) view
class AboutYouUpdate(LoginRequiredMixin, UpdateView):
    model = AboutYou
    form_class = AboutYouForm
    template_name = 'information/edit_about_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        pk_ = self.request.user.aboutyou.pk
        return get_object_or_404(self.model, pk=pk_)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# update of (AboutMe Model) view
class AboutMeUpdate(LoginRequiredMixin, UpdateView):
    model = AboutMe
    form_class = AboutMeForm
    template_name = 'information/edit_about_me.html'

    def get_object(self, queryset=None):
        pk_ = self.request.user.aboutme.pk
        return get_object_or_404(self.model, pk=pk_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['questionary_form'] = AboutMeQuestionaryForm
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        #tera = AboutMeQuestionaryForm(self.request.POST)
        #print(tera)
        return super().form_valid(form)


# update of user profile info (email, first_name, second_name) view
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'information/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('user.profile')
