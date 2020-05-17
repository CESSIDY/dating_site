from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import AboutMe, AboutYou, Gallery
from . import models
from .forms import GalleryForm
from .forms import AboutYouForm, AboutMeForm
import json
from django_select2.views import AutoResponseView
from django.http import HttpResponse


@login_required
def image_delete(request):
    if request.method == 'POST':
        image_pk = request.POST['image_pk']
        Gallery.image_del(image_pk, request.user.pk)
    return redirect('gallery')


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


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Gallery
    form_class = GalleryForm
    queryset = Gallery.objects.all()
    template_name = 'information/create_article.html'

    def get_object(self, queryset=None):
        pk_ = self.kwargs.get('pk')
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


def select2_json_for(model, value):
    results = list()
    values = model.objects.filter(name__startswith=value).values()
    for value in values:
        results.append({'id': value['id'], 'text': value['name']})
    return json.dumps({'err': 'nil', 'results': results})


def heavy_data_about_me(request, model):
    term = request.GET.get("term", )
    Model = {
        'genres': models.Genres,
        'music_types': models.MusicType,
        'films': models.Films,
        'books': models.Books,
        'hobbies': models.Hobbies,
        'foods': models.Foods,
        'countries': models.Countries,
    }[model]

    return HttpResponse(select2_json_for(Model, term), content_type='application/json')
