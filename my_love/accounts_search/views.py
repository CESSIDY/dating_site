from django.shortcuts import render, redirect
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
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
        dt = timezone.now() - relativedelta(days=2)
        if dt > self.request.user.aboutyou.last_search_date:
            context['search_active'] = True
            context['access_date'] = 1
        else:
            last_search_date = self.request.user.aboutyou.last_search_date
            access_date = (datetime.timedelta(days=2) + last_search_date)

            context['access_date'] = str(access_date)
            context['search_active'] = False
        return context


# search of candidates for current user
def partners_search(request):
    dt = timezone.now() - relativedelta(days=2)
    if dt > request.user.aboutyou.last_search_date:
        print("SEARCH!!!!!!")
        users = request.user.search_candidates()

    return HttpResponseRedirect(reverse('accounts_list'))


# show information of User by (pk) view
class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/show.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
