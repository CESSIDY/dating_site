import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from accounts_search.candidates_search_level.Level1 import Level1
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Candidates(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="candidates_creator_set", on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name="candidates_set", on_delete=models.CASCADE)

    def __str__(self):
        return str("{} - {}".format(self.creator, self.candidate))


def search_candidates(self):
    candidates = Level1(self).search()

    return candidates


def get_followers(self):
    followers = Candidates.objects.filter(candidate=self)
    return followers


def get_candidates(self):
    candidates = Candidates.objects.filter(creator=self)
    users = {candidate.candidate for candidate in candidates}
    return users


def make_candidate(self, candidate_id):
    candidate = User.objects.get(pk=candidate_id)
    if candidate.pk != self.pk:
        Candidates.objects.create(
            creator=self,
            candidate=candidate
        ).save()


def remove_candidate(self, candidate_id):
    candidate = User.objects.get(pk=candidate_id)
    Candidates.objects.filter(
        creator=self,
        candidate=candidate
    ).delete()


User.add_to_class("get_followers", get_followers)
User.add_to_class("get_candidates", get_candidates)
User.add_to_class("make_candidate", make_candidate)
User.add_to_class("remove_candidate", remove_candidate)
User.add_to_class("search_candidates", search_candidates)
