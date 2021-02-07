import datetime
from dateutil.relativedelta import relativedelta
import datetime
from django.utils import timezone
from account_settings.models import AboutCommonInfo as commonInfo
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import HStoreField
from accounts_search.candidates_search_level.MainLevel import MainLevel
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


# Candidates model for store a candidates and
# percentage match on different criteria  (like friendship logic)
class Candidates(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="candidates_creator_set", on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name="candidates_set", on_delete=models.CASCADE)
    percentage_similar = HStoreField(blank=True, default=dict)
    common_percentage = models.FloatField(default=0)

    def __str__(self):
        return str("{} - {}".format(self.creator, self.candidate))


# User method for search of candidate (all logic is stored at different levels)
def search_candidates(self):
    # At this level, users will stand up for the main criteria
    main_search_level = MainLevel(self)
    result = main_search_level.updateCandidates()
    return result


# User method what returns all followers from Candidate Model for current user
# followers - these are users who have the current user in the candidate list
def get_followers(self):
    followers = Candidates.objects.filter(candidate=self)
    return followers


# User method what returns all candidates from Candidate Model for current user
# candidates - these are users that are stored in the candidate list for the current user
def get_candidates(self):
    candidates = Candidates.objects.filter(creator=self).order_by('-common_percentage')
    # users = {candidate.candidate for candidate in candidates}
    return candidates


# User method for deleted candidate in candidate model for current user by pk(candidate_id)
def remove_candidate(self, candidate_id):
    candidate = User.objects.get(pk=candidate_id)
    Candidates.objects.filter(
        creator=self,
        candidate=candidate
    ).delete()


def remove_candidates(self):
    Candidates.objects.filter(
        creator=self
    ).delete()


def permission_search_candidates(self):
    return True#timezone.now() > self.get_permission_date_search_candidates()


def get_permission_date_search_candidates(self):
    return timezone.timedelta(days=2) + self.aboutyou.last_search_date


User.add_to_class("permission_search_candidates", permission_search_candidates)
User.add_to_class("get_permission_date_search_candidates", get_permission_date_search_candidates)
User.add_to_class("get_followers", get_followers)
User.add_to_class("get_candidates", get_candidates)
User.add_to_class("remove_candidates", remove_candidates)
User.add_to_class("remove_candidate", remove_candidate)
User.add_to_class("search_candidates", search_candidates)
