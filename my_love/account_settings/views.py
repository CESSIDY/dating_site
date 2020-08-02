from django.contrib.contenttypes.models import ContentType
from django.forms import formset_factory, modelformset_factory
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import AboutMe, AboutYou, Questionary, Question, Answer
from background_data.models import Genres, MusicType, Films, Foods, Countries, Books, Hobbies
from .forms import *
from .questionary import services
from .questionary.settings import form_answer_prefix
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
        context['questionary_forms'] = services.get_aboutYou_edit_form(self.request)
        return context

    def get_object(self, queryset=None):
        pk_ = self.request.user.aboutyou.pk
        return get_object_or_404(self.model, pk=pk_)

    def post(self, request, *args, **kwargs):
        post_context = super().post(request, args, kwargs)
        services.save_questionary_form(request)
        return post_context

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
        context['questionary_forms'] = services.get_aboutMe_edit_form(self.request)
        return context

    def post(self, request, *args, **kwargs):
        post_context = super().post(request, args, kwargs)
        services.save_questionary_form(request)
        return post_context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# update of user profile info (email, first_name, second_name) view
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'information/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('user.profile')


