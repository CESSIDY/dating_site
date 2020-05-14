from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GalleryForm
from account_settings.models import Gallery


class GalleryList(ListView):
    model = Gallery
    context_object_name = 'gallery'
    template_name = 'account/gallery.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _pk = self.request.user.pk
        data = self.model.objects.filter(user=_pk)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GalleryForm()
        return context


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = 'account/about_me.html'


class AboutYouView(LoginRequiredMixin, TemplateView):
    template_name = 'account/about_you.html'
