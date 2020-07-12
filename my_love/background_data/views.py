from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from . import forms


@login_required
# This view for sending the form and saving it, used in an additional browser window,
# when user wont create a some new item.
def store_data(request, model):
    context = {}
    # Get form for current model
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
    # if POST than need save form what come from user
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # status 1 if is valid than additional browser window will be closed
            context['status'] = '1'
    return render(request, 'accounts/{}.html'.format(model), context)


# auxiliary method for searching fields by pattern
def select2_json_for(model, value):
    results = list()
    values = model.objects.filter(name__icontains=value).values()
    # 'id', 'text' are required keys for each field
    for value in values:
        results.append({'id': value['id'], 'text': value['name']})
    return json.dumps({'err': 'nil', 'results': results})


@login_required
# this view used to search and automatic data downloads according to a given template, for the following models
def get_data_by_json(request, model):
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

