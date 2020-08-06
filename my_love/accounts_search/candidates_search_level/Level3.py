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

    def __init__(self, user, candidates):
        self.user = user
        # candidates after level 2
        self.candidates = candidates

    def search(self):
        self.aboutyou_growth()
        self.aboutyou_weight()
        self.aboutme_growth()
        self.aboutme_weight()
        return self.candidates

    def aboutyou_weight(self):
        # add annotate bool_similar_weight field (bool)
        self.candidates = self.candidates.annotate(
            bool_you_similar_weight=Case(
                When(aboutme__weight__range=(self.user.aboutyou.min_weight, self.user.aboutyou.max_weight),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))

    def aboutyou_growth(self):
        # add annotate bool_similar_growth field (bool)
        self.candidates = self.candidates.annotate(
            bool_you_similar_growth=Case(
                When(aboutme__growth__range=(self.user.aboutyou.min_growth, self.user.aboutyou.max_growth),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))

    def aboutme_weight(self):
        # add annotate bool_me_similar_weight field (bool)
        self.candidates = self.candidates.annotate(
            bool_me_similar_weight=Case(
                When(aboutyou__max_weight__gte=self.user.aboutme.weight, then=Value(True)),
                When(aboutyou__min_weight__lte=self.user.aboutme.weight, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))

    def aboutme_growth(self):
        # add annotate bool_me_similar_growth field (bool)
        self.candidates = self.candidates.annotate(
            bool_me_similar_growth=Case(
                When(aboutyou__max_growth__gte=self.user.aboutme.growth, then=Value(True)),
                When(aboutyou__min_growth__lte=self.user.aboutme.growth, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))
