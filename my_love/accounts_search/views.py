from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class AccountsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        users = self.request.user.get_candidates()
        return users


def partners_search(request):
    users = request.user.search_candidates()

    return HttpResponseRedirect(reverse('accounts_list'))


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/show.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
