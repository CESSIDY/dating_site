from django.shortcuts import render, redirect
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
import pytz
from django.contrib.auth.models import User
from .models import Candidates
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages


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
        context['search_active'] = self.request.user.permission_search_candidates()
        context['access_date'] = str(self.request.user.get_permission_date_search_candidates())
        return context


# search of candidates for current user
@login_required
def partners_search(request):
    if request.user.permission_search_candidates():
        result = request.user.search_candidates()
        if result is not True:
            messages.warning(request, result)
    return HttpResponseRedirect(reverse('accounts_list'))

@login_required
def partners_delete(request):
    request.user.remove_candidates()
    return HttpResponseRedirect(reverse('accounts_list'))

# show information of User by (pk) view
class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/show_detail.html'
    model = User
    context_object_name = 'candidate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_accounts'] = SocialAccount.objects.filter(user_id=self.object.pk)
        return context
