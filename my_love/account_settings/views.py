from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import AboutMe, AboutYou
from background_data.models import Genres, MusicType, Films, Foods, Countries, Books, Hobbies
from .forms import AboutYouForm, AboutMeForm, EditProfileForm
import json
from django.http import HttpResponse
from django.views.generic import (
    UpdateView,
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


# auxiliary method for searching fields by pattern
def select2_json_for(model, value):
    results = list()
    values = model.objects.filter(name__icontains=value).values()
    # 'id', 'text' are required keys for each field
    for value in values:
        results.append({'id': value['id'], 'text': value['name']})
    return json.dumps({'err': 'nil', 'results': results})


# this view used to search and automatic data downloads according to a given template, for the following models
def heavy_data_about_me(request, model):
    term = request.GET.get("term", )
    Model = {
        'genres': Genres,
        'music_types': MusicType,
        'films': Films,
        'books': Books,
        'hobbies': Hobbies,
        'foods': Foods,
        'countries': Countries,
    }[model]

    return HttpResponse(select2_json_for(Model, term), content_type='application/json')
