from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class AccountsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        users = self.request.user.get_candidates()
        print(users)
        return users


def partners_search(request):
    print(request.user.search_candidates())
    return HttpResponse('666')


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/show.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
