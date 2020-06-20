from django.shortcuts import render, redirect
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

# search of candidates for current user
def partners_search(request):
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
