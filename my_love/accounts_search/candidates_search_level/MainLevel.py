import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.db import models
from .Level1 import Level1
from .Level2 import Level2
from .Level3 import Level3
from django.db.models import Q
from django.contrib.auth.models import User
from accounts_search import models


class MainLevel:

    def __init__(self, user):
        self.user = user
        # the search will be performed only on active profiles
        self.candidates = User.objects.filter(aboutme__activate=True)

    def updateCandidates(self):
        self.search()
        self.makeCandidates()

    def search(self):
        self.candidates = Level1(self.user, self.candidates).search()
        print(self.candidates)
        # At this level users will not defend, but will sum up at the expense
        # of coincidences in percent for each field
        self.candidates = Level2(self.user, self.candidates).search()
        print(self.candidates)
        # At this level, only those fields are presented, in the comparison of which,u
        # it is possible to give an unambiguous answer, true or false.
        self.candidates = Level3(self.user, self.candidates).search()

    def getPercentageDictionary(self):
        # Take from current user field whit useful information
        mePercentage = self.getAboutMePercentageDictionary()
        youPercentage = self.getAboutYouPercentageDictionary()
        mePercentage.update(youPercentage)
        return mePercentage

    def makeCandidates(self):
        models.Candidates.objects.filter(creator=self.user).delete()
        for candidate in self.candidates:
            if candidate.pk != self.user.pk:
                obj, created = models.Candidates.objects.update_or_create(
                    creator=self.user, candidate=candidate,
                    defaults={
                        'percentage_similar': self.getPercentageDictionary()
                    },
                )
        self.user.aboutyou.save()
        self.user.aboutme.save()

    def getAboutYouPercentageDictionary(self):
        prcentage = dict
        hobbies = self.user.aboutyou.hobbies.count()
        music_types = self.user.aboutyou.music_types.count()
        foods = self.user.aboutyou.foods.count()
        books = self.user.aboutyou.books.count()
        films = self.user.aboutyou.films.count()
        genres = self.user.aboutyou.genres.count()
        questionary = self.user.questionarys.count()
        for candidate in self.candidates:
            if candidate.pk != self.user.pk:
                # for each field there is a comparison to find a percentage match and this value will be stored in database
                # user = User.objects.get(pk=candidate.pk)
                percentage_similar_hobbies = (100 - ((hobbies - candidate.count_you_similar_hobbies) / (hobbies / 100)))
                percentage_similar_music_types = (100 - ((music_types - candidate.count_you_similar_music_types) / (
                        music_types / 100)))
                percentage_similar_foods = (100 - ((foods - candidate.count_you_similar_foods) / (foods / 100)))
                percentage_similar_books = (100 - ((books - candidate.count_you_similar_books) / (books / 100)))
                percentage_similar_films = (100 - ((films - candidate.count_you_similar_films) / (films / 100)))
                percentage_similar_genres = (100 - ((genres - candidate.count_you_similar_genres) / (genres / 100)))
                percentage_similar_answers = (
                        100 - ((questionary - candidate.count_you_similar_questionary) / (questionary / 100)))
                percentage_similar_weight = (100 if candidate.bool_you_similar_weight else 0)
                percentage_similar_growth = (100 if candidate.bool_you_similar_growth else 0)
                prcentage = {
                    'you_hobbies': percentage_similar_hobbies,
                    'you_music_types': percentage_similar_music_types,
                    'you_foods': percentage_similar_foods,
                    'you_books': percentage_similar_books,
                    'you_films': percentage_similar_films,
                    'you_genres': percentage_similar_genres,
                    'you_weight': percentage_similar_weight,
                    'you_growth': percentage_similar_growth,
                    'you_answers': percentage_similar_answers}
        return prcentage

    def getAboutMePercentageDictionary(self):
        prcentage = dict
        hobbies = self.user.aboutme.hobbies.count()
        music_types = self.user.aboutme.music_types.count()
        foods = self.user.aboutme.foods.count()
        books = self.user.aboutme.books.count()
        films = self.user.aboutme.films.count()
        genres = self.user.aboutme.genres.count()
        questionary = self.user.questionarys.count()
        for candidate in self.candidates:
            if candidate.pk != self.user.pk:
                # for each field there is a comparison to find a percentage match and this value will be stored in database
                # user = User.objects.get(pk=candidate.pk)
                percentage_similar_hobbies = (100 - ((hobbies - candidate.count_me_similar_hobbies) / (hobbies / 100)))
                percentage_similar_music_types = (100 - ((music_types - candidate.count_me_similar_music_types) / (
                        music_types / 100)))
                percentage_similar_foods = (100 - ((foods - candidate.count_me_similar_foods) / (foods / 100)))
                percentage_similar_books = (100 - ((books - candidate.count_me_similar_books) / (books / 100)))
                percentage_similar_films = (100 - ((films - candidate.count_me_similar_films) / (films / 100)))
                percentage_similar_genres = (100 - ((genres - candidate.count_me_similar_genres) / (genres / 100)))
                percentage_similar_answers = (
                        100 - ((questionary - candidate.count_me_similar_questionary) / (questionary / 100)))
                percentage_similar_weight = (100 if candidate.bool_me_similar_weight else 0)
                percentage_similar_growth = (100 if candidate.bool_me_similar_growth else 0)
                prcentage = {
                    'me_hobbies': percentage_similar_hobbies,
                    'me_music_types': percentage_similar_music_types,
                    'me_foods': percentage_similar_foods,
                    'me_books': percentage_similar_books,
                    'me_films': percentage_similar_films,
                    'me_genres': percentage_similar_genres,
                    'me_weight': percentage_similar_weight,
                    'me_growth': percentage_similar_growth,
                    'me_answers': percentage_similar_answers}
        return prcentage
