from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Gallery
from .forms import GalleryForm
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)


# deleted one article of (Gallery Model) vie
class ArticleDelete(LoginRequiredMixin, DeleteView):
    template_name = 'delete_article.html'

    def get_object(self, queryset=None):
        pk_ = self.kwargs.get("pk")
        return get_object_or_404(Gallery, pk=pk_)

    def get_success_url(self):
        return reverse('gallery')


# create one article of (Gallery Model) view
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Gallery
    form_class = GalleryForm
    template_name = 'create_article.html'

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
    template_name = 'create_article.html'

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
