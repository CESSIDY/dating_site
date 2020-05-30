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
        return self.candidates

    def filterHobbies(self, hobbie):
        if hobbie in self.user.aboutyou.hobbies:
            return True
        else:
            return False

    def aboutyou_hobbies(self):
        print(self.user.aboutyou.hobbies.all())
        # above_5 = Count('book', filter=Q(book__rating__gt=5))
        self.candidates = self.candidates.annotate(
            count_similar_hobbis=Count('aboutme__hobbies', filter=Q(aboutme__hobbies__in=self.user.aboutyou.hobbies.all()))
        )
        #         self.candidates.annotate(
        #             count_similar_hobbis=Q('aboutme__hobbies' in self.user.aboutyou.hobbies.all())
        #         )
        #
