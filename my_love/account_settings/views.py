from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import AboutMe, AboutYou, Gallery
from background_data.models import Genres, MusicType, Films, Foods, Countries, Books, Hobbies
from .forms import GalleryForm
from .forms import AboutYouForm, AboutMeForm
import json
from django_select2.views import AutoResponseView
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)


# @login_required

# deleted one article of (Gallery Model) vie
class ArticleDelete(DeleteView):
    template_name = 'information/delete_article.html'

    def get_object(self, queryset=None):
        pk_ = self.kwargs.get("pk")
        return get_object_or_404(Gallery, pk=pk_)

    def get_success_url(self):
        return reverse('gallery')


# create one article of (Gallery Model) view
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Gallery
    form_class = GalleryForm
    template_name = 'information/create_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('gallery')


# update one article of (Gallery Model) view
class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Gallery
    form_class = GalleryForm
    queryset = Gallery.objects.all()
    template_name = 'information/create_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_url'] = context['gallery'].path.url
        return context

    def get_object(self, queryset=None):
        pk_ = self.kwargs.get('pk')
        # check whether the user edits his article
        if pk_ is not None or pk_.isnumeric():
            article = self.model.objects.get(id=pk_)
            if article.user == self.request.user:
                return article

        return None

    def form_valid(self, form):
        if self.request.user.gallery_set.filter(pk=form.instance.pk):
            form.instance.user = self.request.user
            return super().form_valid(form)
        return None

    def get_success_url(self):
        return reverse('gallery')


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
