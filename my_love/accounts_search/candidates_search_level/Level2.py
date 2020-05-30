import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import FilteredRelation, Q, Count, F
from django.db.models import Case, IntegerField, Value, When


class Level2:

    # конструктор
    def __init__(self, user, candidates):
        self.user = user
        self.candidates = candidates

    def search(self):
        self.aboutyou_hobbies()
        self.aboutyou_music_types()
        self.aboutyou_foods()
        self.aboutyou_genres()
        self.aboutyou_films()
        self.aboutyou_books()
        return self.candidates

    def aboutyou_books(self):
        self.candidates = self.candidates.annotate(
            count_similar_books=Count('aboutme__books',
                                      filter=Q(aboutme__books__in=self.user.aboutyou.books.all()), distinct=True)
        )

    def aboutyou_films(self):
        self.candidates = self.candidates.annotate(
            count_similar_films=Count('aboutme__films',
                                      filter=Q(aboutme__films__in=self.user.aboutyou.films.all()), distinct=True)
        )

    def aboutyou_genres(self):
        self.candidates = self.candidates.annotate(
            count_similar_genres=Count('aboutme__genres',
                                       filter=Q(aboutme__genres__in=self.user.aboutyou.genres.all()), distinct=True)
        )

    def aboutyou_foods(self):
        self.candidates = self.candidates.annotate(
            count_similar_foods=Count('aboutme__foods',
                                      filter=Q(aboutme__foods__in=self.user.aboutyou.foods.all()), distinct=True)
        )

    def aboutyou_music_types(self):
        self.candidates = self.candidates.annotate(
            count_similar_music_types=Count('aboutme__music_types',
                                            filter=Q(aboutme__music_types__in=self.user.aboutyou.music_types.all()),
                                            distinct=True)
        )

    def aboutyou_hobbies(self):
        # if you have some bag or error try this:
        # self.candidates = self.candidates.all().annotate(
        self.candidates = self.candidates.annotate(
            count_similar_hobbies=Count('aboutme__hobbies',
                                        filter=Q(aboutme__hobbies__in=self.user.aboutyou.hobbies.all()), distinct=True)
        )
