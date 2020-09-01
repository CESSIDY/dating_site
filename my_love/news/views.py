from django.http import HttpResponse
from .services import News
import json
from django.shortcuts import render
from django.utils.safestring import mark_safe

from django.shortcuts import render


def newsGenerate(request):
    #news = News(request).generate()
    return HttpResponse(status=200)

def chat(request):
    """Главная страница"""
    return render(request, 'chat/chat.html', {})


def room(request, room_name):
    """"""
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })