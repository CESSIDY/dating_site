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
        print(users)
        return users


def partners_search(request):
    users = request.user.search_candidates()
    print('= Hobbies: {}. Me about You: {}. Partners: {}'.format(
        users[0].count_similar_hobbies,
        request.user.aboutyou.hobbies.all(),
        users[0].aboutme.hobbies.all()))
    print('= Music Types: {}. Me about You: {}. Partners: {}'.format(
        users[0].count_similar_music_types,
        request.user.aboutyou.music_types.all(),
        users[0].aboutme.music_types.all()))
    print('= Foods Types: {}. Me about You: {}. Partners: {}'.format(
        users[0].count_similar_foods,
        request.user.aboutyou.foods.all(),
        users[0].aboutme.foods.all()))
    print('= Books Types: {}. Me about You: {}. Partners: {}'.format(
        users[0].count_similar_books,
        request.user.aboutyou.books.all(),
        users[0].aboutme.books.all()))
    print('= Films Types: {}. Me about You: {}. Partners: {}'.format(
        users[0].count_similar_films,
        request.user.aboutyou.films.all(),
        users[0].aboutme.films.all()))
    print('= Genres Types: {}. Me about You: {}. Partners: {}'.format(
        users[0].count_similar_genres,
        request.user.aboutyou.genres.all(),
        users[0].aboutme.genres.all()))
    print('= Weight: {}. Me about You: {} - {}. Partners: {}'.format(users[0].bool_similar_weight,
                                                                     request.user.aboutyou.min_weight,
                                                                     request.user.aboutyou.max_weight,
                                                                     users[0].aboutme.weight))
    print('= Growth: {}. Me about You: {} - {}. Partners: {}'.format(users[0].bool_similar_growth,
                                                                     request.user.aboutyou.min_growth,
                                                                     request.user.aboutyou.max_growth,
                                                                     users[0].aboutme.growth))
    print('= Name: {}'.format(users[0].aboutme.name))

    return HttpResponseRedirect(reverse('accounts_list'))


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/show.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
