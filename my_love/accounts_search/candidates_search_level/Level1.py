import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date

class Level1:

    def __init__(self, user, candidates):
        self.user = user
        self.candidates = candidates

    def search(self):
        # we will exclude users of inappropriate age, by criteria for current user in (AboutYou model)
        self.aboutyou_age()
        # we will exclude users of inappropriate gander, by criteria for current user in (AboutYou model)
        self.aboutyou_gender()
        # we will exclude users of inappropriate countries, by criteria for current user in (AboutYou model)
        self.aboutyou_countries()
        self.aboutme_age()
        self.aboutme_gender()
        self.aboutme_countries()
        return self.candidates

    def aboutyou_age(self):
        # make years in date
        if self.user.aboutyou.min_age is not None:
            upper_date = datetime.datetime.now() - relativedelta(years=self.user.aboutyou.min_age)
        else:
            upper_date = datetime.datetime.now()
        if self.user.aboutyou.max_age is not None:
            lower_date = datetime.datetime.now() - relativedelta(years=self.user.aboutyou.max_age)
        else:
            lower_date = datetime.datetime.now() - relativedelta(years=100)

        self.candidates = self.candidates.filter(aboutme__birthday__range=(lower_date, upper_date))

    def aboutyou_gender(self):
        if self.user.aboutyou.gender == commonInfo.DEFAULT_VAL:
            candidates = self.candidates.filter(
                Q(aboutme__gender=commonInfo.FEMALE) | Q(aboutme__gender=commonInfo.MALL))
        else:
            self.candidates = self.candidates.filter(aboutme__gender=self.user.aboutyou.gender)

    def aboutyou_countries(self):
        countries_pk = self.user.aboutyou.countries.values_list('pk')
        self.candidates = self.candidates.filter(aboutme__country__in=countries_pk)

    def aboutme_age(self):
        age = self.calculate_age(self.user.aboutme.birthday)
        self.candidates = self.candidates.filter(Q(aboutyou__min_age__gte=age) | Q(aboutyou__min_age__lte=age))

    def aboutme_gender(self):
        if self.user.aboutyou.gender == commonInfo.DEFAULT_VAL:
            candidates = self.candidates.filter(
                Q(aboutyou__gender=commonInfo.FEMALE) | Q(aboutyou__gender=commonInfo.MALL))
        else:
            self.candidates = self.candidates.filter(aboutyou__gender=self.user.aboutme.gender)

    def aboutme_countries(self):
        country_pk = self.user.aboutme.country.pk
        self.candidates = self.candidates.filter(aboutyou__countries__pk__contains=country_pk)

    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
