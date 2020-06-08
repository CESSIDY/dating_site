import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import FilteredRelation, Q, Count, F
from django.db.models import Case, BooleanField, Value, When


class Level3:

    # конструктор
    def __init__(self, user, candidates):
        self.user = user
        self.candidates = candidates

    def search(self):
        self.aboutyou_growth()
        self.aboutyou_weight()
        return self.candidates

    def aboutyou_weight(self):
        self.candidates = self.candidates.annotate(
            bool_similar_weight=Case(
                When(aboutme__weight__range=(self.user.aboutyou.min_weight, self.user.aboutyou.max_weight),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))

    def aboutyou_growth(self):
        self.candidates = self.candidates.annotate(
            bool_similar_growth=Case(
                When(aboutme__growth__range=(self.user.aboutyou.min_growth, self.user.aboutyou.max_growth),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))
