from django.shortcuts import render, redirect
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import pytz
from django.contrib.auth.models import User
from .models import Candidates
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


# list of candidates for the current user
class AccountsListView(LoginRequiredMixin, ListView):
    model = Candidates
    template_name = 'accounts/list.html'
    context_object_name = 'candidates'

    def get_queryset(self):
        # get list of candidates for current user
        candidates = self.request.user.get_candidates()
        return candidates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_search_date = self.request.user.aboutyou.last_search_date
        access_date = timezone.timedelta(days=2) + last_search_date
        if timezone.now() > access_date:
            context['search_active'] = True
            context['access_date'] = 1
        else:
            context['search_active'] = False
            context['access_date'] = str(access_date)
        return context


# search of candidates for current user
def partners_search(request):
    last_search_date = request.user.aboutyou.last_search_date
    access_date = timezone.timedelta(days=2) + last_search_date
    if timezone.now() > access_date:
        request.user.search_candidates()

    return HttpResponseRedirect(reverse('accounts_list'))


# show information of User by (pk) view
class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/show_detail.html'
    model = User
    context_object_name = 'candidate'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
