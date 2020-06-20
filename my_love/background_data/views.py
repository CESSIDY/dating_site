from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import forms


@login_required
# This view for sending the form and saving it, used in an additional browser window,
# when user wont create a some new item.
def upload_data(request, model):
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

