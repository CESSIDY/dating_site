from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import AboutMe, AboutYou, Gallery
from . import models
from account_show.forms import GalleryForm
from .forms import AboutYouForm, AboutMeForm
import json
from django_select2.views import AutoResponseView
from django.http import HttpResponse


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_image.name, uploaded_image)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


@login_required
def image_upload(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            form.save_m2m()
    return redirect('gallery')


@login_required
def image_delete(request):
    if request.method == 'POST':
        image_pk = request.POST['image_pk']
        Gallery.image_del(image_pk, request.user.pk)
    return redirect('gallery')


class AboutYouUpdate(LoginRequiredMixin, UpdateView):
    model = AboutYou
    form_class = AboutYouForm
    template_name = 'information/edit_about_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("TERA")
        #print(context['form']['color_hair'])
        #unit_id = context['latest_articles']
        #form.fields['unit_id'].choices = [(unit_id, unit_id)]
        #context['color_hair'] = context['color_hair']
        #context['color_aye'] = context['color_aye']
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
