from django.contrib.auth.models import User
from django.views.generic import ListView
from django.shortcuts import render

# https://github.com/codingforentrepreneurs/Try-Django/tree/master/src
def home(request):
    user_count = User.objects.count()
    return render(request, 'home.html', {'user_count': user_count})

