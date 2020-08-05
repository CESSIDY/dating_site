import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.models import ContentType
from account_settings.models import AboutCommonInfo as commonInfo, AboutYou
from django.db import models
from account_settings.models import Questionary, Question, Answer
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
        obj_type = ContentType.objects.get_for_model(AboutYou)
        answers = Answer.objects.filter(
            pk__in=Questionary.objects.filter(user=self.user, content_type=obj_type).values('answer'))
        self.candidates = self.candidates.annotate(
            count_similar_questionary=Count('questionary__pk', filter=Q(questionary__answer__in=answers),
                                            distinct=True))
