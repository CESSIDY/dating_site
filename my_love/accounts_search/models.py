import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import HStoreField
from accounts_search.candidates_search_level.Level1 import Level1
from accounts_search.candidates_search_level.Level2 import Level2
from accounts_search.candidates_search_level.Level3 import Level3
from accounts_search.candidates_search_level.Level4 import Level4
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

    def __str__(self):
        return str("{} - {}".format(self.creator, self.candidate))

    # return common percentage of all fields
    def common_percentage(self):
        all_percentages = 0
        for percentage in self.percentage_similar.values():
            all_percentages += float(percentage)
        commonProcent = (all_percentages / len(self.percentage_similar))
        return round(commonProcent, 2)


# User method for search of candidate (all logic is stored at different levels)
def search_candidates(self):
    # At this level, users will stand up for the main criteria
    candidates = Level1(self).search()
    # At this level users will not defend, but will sum up at the expense
    # of coincidences in percent for each field
    candidates = Level2(self, candidates).search()
    # At this level, only those fields are presented, in the comparison of which,u
    # it is possible to give an unambiguous answer, true or false.
    candidates = Level3(self, candidates).search()

    candidates = Level4(self, candidates).search()

    # call of method for store all candidates(users) in candidate model for current user
    self.make_candidates(candidates)
    self.aboutyou.save()


# User method what returns all followers from Candidate Model for current user
# followers - these are users who have the current user in the candidate list
def get_followers(self):
    followers = Candidates.objects.filter(candidate=self)
    return followers


# User method what returns all candidates from Candidate Model for current user
# candidates - these are users that are stored in the candidate list for the current user
def get_candidates(self):
    candidates = Candidates.objects.filter(creator=self)
    # users = {candidate.candidate for candidate in candidates}
    return candidates


# User method for stores candidates(users) in candidate model for current user
def make_candidates(self, candidates):
    # Take from current user field whit useful information
    hobbies = self.aboutyou.hobbies.count()
    music_types = self.aboutyou.music_types.count()
    foods = self.aboutyou.foods.count()
    books = self.aboutyou.books.count()
    films = self.aboutyou.films.count()
    genres = self.aboutyou.genres.count()
    questionary = self.questionarys.count()
    for candidate in candidates:
        if candidate.pk != self.pk:
            # for each field there is a comparison to find a percentage match and this value will be stored in database
            # user = User.objects.get(pk=candidate.pk)
            percentage_similar_hobbies = (100 - ((hobbies - candidate.count_similar_hobbies) / (hobbies / 100)))
            percentage_similar_music_types = (100 - ((music_types - candidate.count_similar_music_types) / (
                    music_types / 100)))
            percentage_similar_foods = (100 - ((foods - candidate.count_similar_foods) / (foods / 100)))
            percentage_similar_books = (100 - ((books - candidate.count_similar_books) / (books / 100)))
            percentage_similar_films = (100 - ((films - candidate.count_similar_films) / (films / 100)))
            percentage_similar_genres = (100 - ((genres - candidate.count_similar_genres) / (genres / 100)))
            percentage_similar_answers = (
                    100 - ((questionary - candidate.count_similar_questionary) / (questionary / 100)))
            percentage_similar_weight = (100 if candidate.bool_similar_weight else 0)
            percentage_similar_growth = (100 if candidate.bool_similar_growth else 0)
            obj, created = Candidates.objects.update_or_create(
                creator=self, candidate=candidate,
                defaults={
                    'percentage_similar': {
                        'hobbies': percentage_similar_hobbies,
                        'music_types': percentage_similar_music_types,
                        'foods': percentage_similar_foods,
                        'books': percentage_similar_books,
                        'films': percentage_similar_films,
                        'genres': percentage_similar_genres,
                        'weight': percentage_similar_weight,
                        'growth': percentage_similar_growth,
                        'answers': percentage_similar_answers}
                },
            )


# User method for deleted candidate in candidate model for current user by pk(candidate_id)
def remove_candidate(self, candidate_id):
    candidate = User.objects.get(pk=candidate_id)
    Candidates.objects.filter(
        creator=self,
        candidate=candidate
    ).delete()


User.add_to_class("get_followers", get_followers)
User.add_to_class("get_candidates", get_candidates)
User.add_to_class("make_candidates", make_candidates)
User.add_to_class("remove_candidate", remove_candidate)
User.add_to_class("search_candidates", search_candidates)
