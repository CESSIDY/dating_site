import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import FilteredRelation, Q, Count, F
from django.db.models import Case, IntegerField, Value, When


class Level4:

    def __init__(self, user, candidates):
        self.user = user
        # candidates after level 3
        self.candidates = candidates

    def search(self):
        self.aboutyou_questionary()
        return self.candidates

    def aboutyou_questionary(self):

        self.candidates = self.candidates.annotate(
            count_similar_questionary=1
        )
