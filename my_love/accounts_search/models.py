import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from accounts_search.candidates_search_level.Level1 import Level1
from accounts_search.candidates_search_level.Level2 import Level2
from accounts_search.candidates_search_level.Level3 import Level3
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Candidates(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="candidates_creator_set", on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name="candidates_set", on_delete=models.CASCADE)
    percentage_similar_hobbies = models.FloatField(default=0)
    percentage_similar_music_types = models.FloatField(default=0)
    percentage_similar_foods = models.FloatField(default=0)
    percentage_similar_books = models.FloatField(default=0)
    percentage_similar_films = models.FloatField(default=0)
    percentage_similar_genres = models.FloatField(default=0)
    percentage_similar_weight = models.FloatField(default=0)
    percentage_similar_growth = models.FloatField(default=0)

    def __str__(self):
        return str("{} - {}".format(self.creator, self.candidate))


def search_candidates(self):
    candidates = Level1(self).search()
    candidates = Level2(self, candidates).search()
    candidates = Level3(self, candidates).search()

    print('= Hobbies: {}. Me about You: {}. Partners: {}'.format(
        candidates[0].count_similar_hobbies,
        self.aboutyou.hobbies.all(),
        candidates[0].aboutme.hobbies.all()))
    print('= Music Types: {}. Me about You: {}. Partners: {}'.format(
        candidates[0].count_similar_music_types,
        self.aboutyou.music_types.all(),
        candidates[0].aboutme.music_types.all()))
    print('= Foods Types: {}. Me about You: {}. Partners: {}'.format(
        candidates[0].count_similar_foods,
        self.aboutyou.foods.all(),
        candidates[0].aboutme.foods.all()))
    print('= Books Types: {}. Me about You: {}. Partners: {}'.format(
        candidates[0].count_similar_books,
        self.aboutyou.books.all(),
        candidates[0].aboutme.books.all()))
    print('= Films Types: {}. Me about You: {}. Partners: {}'.format(
        candidates[0].count_similar_films,
        self.aboutyou.films.all(),
        candidates[0].aboutme.films.all()))
    print('= Genres Types: {}. Me about You: {}. Partners: {}'.format(
        candidates[0].count_similar_genres,
        self.aboutyou.genres.all(),
        candidates[0].aboutme.genres.all()))
    print('= Weight: {}. Me about You: {} - {}. Partners: {}'.format(candidates[0].bool_similar_weight,
                                                                     self.aboutyou.min_weight,
                                                                     self.aboutyou.max_weight,
                                                                     candidates[0].aboutme.weight))
    print('= Growth: {}. Me about You: {} - {}. Partners: {}'.format(candidates[0].bool_similar_growth,
                                                                     self.aboutyou.min_growth,
                                                                     self.aboutyou.max_growth,
                                                                     candidates[0].aboutme.growth))
    print('= Name: {}'.format(candidates[0].aboutme.name))

    self.make_candidates(candidates)
    return candidates


def get_followers(self):
    followers = Candidates.objects.filter(candidate=self)
    return followers


def get_candidates(self):
    candidates = Candidates.objects.filter(creator=self)
    users = {candidate.candidate for candidate in candidates}
    return users


def make_candidates(self, candidates):
    hobbies = self.aboutyou.hobbies.count()
    music_types = self.aboutyou.music_types.count()
    foods = self.aboutyou.foods.count()
    books = self.aboutyou.books.count()
    films = self.aboutyou.films.count()
    genres = self.aboutyou.genres.count()
    for candidate in candidates:
        if candidate.pk != self.pk:
            # user = User.objects.get(pk=candidate.pk)
            percentage_similar_hobbies = (100 - ((hobbies - candidate.count_similar_hobbies) / (hobbies / 100)))
            percentage_similar_music_types = (100 - ((music_types - candidate.count_similar_music_types) / (
                    music_types / 100)))
            percentage_similar_foods = (100 - ((foods - candidate.count_similar_foods) / (foods / 100)))
            percentage_similar_books = (100 - ((books - candidate.count_similar_books) / (books / 100)))
            percentage_similar_films = (100 - ((films - candidate.count_similar_films) / (films / 100)))
            percentage_similar_genres = (100 - ((genres - candidate.count_similar_genres) / (genres / 100)))
            percentage_similar_weight = (100 if candidate.bool_similar_weight else 0)
            percentage_similar_growth = (100 if candidate.bool_similar_growth else 0)
            obj, created = Candidates.objects.update_or_create(
                creator=self, candidate=candidate,
                defaults={
                    'percentage_similar_hobbies': percentage_similar_hobbies,
                    'percentage_similar_music_types': percentage_similar_music_types,
                    'percentage_similar_foods': percentage_similar_foods,
                    'percentage_similar_books': percentage_similar_books,
                    'percentage_similar_films': percentage_similar_films,
                    'percentage_similar_genres': percentage_similar_genres,
                    'percentage_similar_weight': percentage_similar_weight,
                    'percentage_similar_growth': percentage_similar_growth,
                },
            )


def make_candidate(self, candidate_id):
    candidate = User.objects.get(pk=candidate_id)
    if candidate.pk != self.pk:
        Candidates.objects.create(
            creator=self,
            candidate=candidate
        ).save()


def remove_candidate(self, candidate_id):
    candidate = User.objects.get(pk=candidate_id)
    Candidates.objects.filter(
        creator=self,
        candidate=candidate
    ).delete()


User.add_to_class("get_followers", get_followers)
User.add_to_class("get_candidates", get_candidates)
User.add_to_class("make_candidate", make_candidate)
User.add_to_class("make_candidates", make_candidates)
User.add_to_class("remove_candidate", remove_candidate)
User.add_to_class("search_candidates", search_candidates)
