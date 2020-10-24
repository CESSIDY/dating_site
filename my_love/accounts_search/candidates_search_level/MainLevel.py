import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo, AboutMe, AboutYou
from django.contrib.contenttypes.models import ContentType
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
        self.hobbies = self.user.aboutyou.hobbies.count()
        self.music_types = self.user.aboutyou.music_types.count()
        self.foods = self.user.aboutyou.foods.count()
        self.books = self.user.aboutyou.books.count()
        self.films = self.user.aboutyou.films.count()
        self.genres = self.user.aboutyou.genres.count()
        self.questionary_me = self.user.questionarys.filter(
            content_type=ContentType.objects.get_for_model(AboutMe)).count()
        self.questionary_you = self.user.questionarys.filter(
            content_type=ContentType.objects.get_for_model(AboutYou)).count()
        # the search will be performed only on active profiles
        self.candidates = User.objects.filter(aboutme__activate=True)

    def updateCandidates(self):
        self.search()
        self.makeCandidates()

    def search(self):
        self.candidates = Level1(self.user, self.candidates).search()
        # At this level users will not defend, but will sum up at the expense
        # of coincidences in percent for each field
        self.candidates = Level2(self.user, self.candidates).search()
        # At this level, only those fields are presented, in the comparison of which,u
        # it is possible to give an unambiguous answer, true or false.
        self.candidates = Level3(self.user, self.candidates).search()

    def getPercentageDictionary(self, candidate):
        # Take from current user field whit useful information
        mePercentage = self.getAboutMePercentageDictionary(candidate)
        youPercentage = self.getAboutYouPercentageDictionary(candidate)
        mePercentage.update(youPercentage)
        return mePercentage

    def makeCandidates(self):
        models.Candidates.objects.filter(creator=self.user).delete()
        for candidate in self.candidates:
            if candidate.pk != self.user.pk:
                percentage_dictionary = self.getPercentageDictionary(candidate)
                common_percentage = self.commonPercentage(percentage_dictionary)
                obj, created = models.Candidates.objects.update_or_create(
                    creator=self.user, candidate=candidate,
                    defaults={
                        'percentage_similar': percentage_dictionary,
                        'common_percentage': common_percentage
                    },
                )
        self.user.aboutyou.save()
        self.user.aboutme.save()

    def commonPercentage(self, percentageDictionary):
        all_percentages = 0
        for percentage in percentageDictionary.values():
            all_percentages += float(percentage)
        commonProcent = (all_percentages / len(percentageDictionary))
        return round(commonProcent, 2)

    def getAboutYouPercentageDictionary(self, candidate):
        percentage_similar_hobbies = (
                100 - ((self.hobbies - candidate.count_you_similar_hobbies) / (self.hobbies / 100)))
        percentage_similar_music_types = (
                100 - ((self.music_types - candidate.count_you_similar_music_types) / (self.music_types / 100)))
        percentage_similar_foods = (
                100 - ((self.foods - candidate.count_you_similar_foods) / (self.foods / 100)))
        percentage_similar_books = (
                100 - ((self.books - candidate.count_you_similar_books) / (self.books / 100)))
        percentage_similar_films = (
                100 - ((self.films - candidate.count_you_similar_films) / (self.films / 100)))
        percentage_similar_genres = (
                100 - ((self.genres - candidate.count_you_similar_genres) / (self.genres / 100)))
        percentage_similar_answers = (
                100 - ((self.questionary_you - candidate.count_you_similar_questionary) / (self.questionary_you / 100)))
        percentage_similar_weight = (100 if candidate.bool_you_similar_weight else 0)
        percentage_similar_growth = (100 if candidate.bool_you_similar_growth else 0)
        return {
            'you_hobbies': percentage_similar_hobbies,
            'you_music_types': percentage_similar_music_types,
            'you_foods': percentage_similar_foods,
            'you_books': percentage_similar_books,
            'you_films': percentage_similar_films,
            'you_genres': percentage_similar_genres,
            'you_weight': percentage_similar_weight,
            'you_growth': percentage_similar_growth,
            'you_answers': percentage_similar_answers}

    def getAboutMePercentageDictionary(self, candidate):
        percentage_similar_hobbies = (
                100 - ((self.hobbies - candidate.count_me_similar_hobbies) / (self.hobbies / 100)))
        percentage_similar_music_types = (100 - ((self.music_types - candidate.count_me_similar_music_types) / (
                self.music_types / 100)))
        percentage_similar_foods = (
                100 - ((self.foods - candidate.count_me_similar_foods) / (self.foods / 100)))
        percentage_similar_books = (
                100 - ((self.books - candidate.count_me_similar_books) / (self.books / 100)))
        percentage_similar_films = (
                100 - ((self.films - candidate.count_me_similar_films) / (self.films / 100)))
        percentage_similar_genres = (
                100 - ((self.genres - candidate.count_me_similar_genres) / (self.genres / 100)))
        percentage_similar_answers = (
                100 - ((self.questionary_me - candidate.count_me_similar_questionary) / (self.questionary_me / 100)))
        percentage_similar_weight = (100 if candidate.bool_me_similar_weight else 0)
        percentage_similar_growth = (100 if candidate.bool_me_similar_growth else 0)
        return {
            'me_hobbies': percentage_similar_hobbies,
            'me_music_types': percentage_similar_music_types,
            'me_foods': percentage_similar_foods,
            'me_books': percentage_similar_books,
            'me_films': percentage_similar_films,
            'me_genres': percentage_similar_genres,
            'me_weight': percentage_similar_weight,
            'me_growth': percentage_similar_growth,
            'me_answers': percentage_similar_answers}
