from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import forms


@login_required
def upload_data(request, model):
    context = {}
    form = {
        'genres': forms.GenresForm(request.POST),
        'music_types': forms.MusicTypesForm(request.POST),
        'films': forms.FilmsForm(request.POST),
        'books': forms.BooksForm(request.POST),
        'hobbies': forms.HobbiesForm(request.POST),
        'foods': forms.FoodsForm(request.POST),
        'countries': forms.CountriesForm(request.POST),
    }[model]
    context['form'] = form
    context['status'] = '0'
    if request.method == 'POST':
        data = {'status': 'false'}
        if form.is_valid():
            form.save()
            context['status'] = '1'
    return render(request, 'accounts/{}.html'.format(model), context)

