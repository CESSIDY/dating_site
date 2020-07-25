from django.shortcuts import render
from django.urls import reverse
from .models import Like
from django.http import HttpResponse, HttpResponseNotFound
import json
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import BaseDetailView
from .services import *
from articles_settings.models import *
from .JSONResponseMixin import JSONResponseMixin


# auxiliary method for searching fields by pattern
@login_required
def like(request, pk):
    user = request.user
    article = Gallery.objects.get(pk=pk)
    if is_fan(article, user):
        remove_like(article, user)
        return HttpResponse(json.dumps({'status': 'false', 'pk': pk}), content_type='application/json')
    else:
        add_like(article, user)
        return HttpResponse(json.dumps({'status': 'true', 'pk': pk}), content_type='application/json')
