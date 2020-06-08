import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Level1:

    # конструктор
    def __init__(self, user):
        self.user = user
        self.candidates = User.objects.filter(aboutme__activate=True)

    def search(self):
        self.aboutyou_age()
        self.aboutyou_gender()
        self.aboutyou_countries()
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
        tera = self.user.aboutyou.countries.values_list('pk')
        self.candidates = self.candidates.filter(aboutme__country__in=tera)
