from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GalleryForm
from allauth.socialaccount.forms import SignupForm
from articles_settings.models import Gallery
from allauth.socialaccount.models import SocialAccount


# show articles list of (Gallery Model) view for current user
class GalleryList(LoginRequiredMixin, ListView):
    model = Gallery
    context_object_name = 'gallery'
    template_name = 'account/gallery.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _pk = self.request.user.pk
        data = self.model.objects.filter(user=_pk).order_by('-pub_date')
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GalleryForm()
        return context


# show information of (AboutMe Model) view for current user
class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = 'account/about_me.html'


# show information of (AboutYou Model) view for current user
class AboutYouView(LoginRequiredMixin, TemplateView):
    template_name = 'account/about_you.html'


class UserProfileInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        social_accounts = SocialAccount.objects.filter(user_id=self.request.user.id)
        context['social_accounts'] = social_accounts
        return context
