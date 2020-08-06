import datetime
from dateutil.relativedelta import relativedelta
from account_settings.models import Questionary, Question, Answer, AboutYou, AboutMe
from django.contrib.contenttypes.models import ContentType
from account_settings.models import AboutCommonInfo as commonInfo
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import FilteredRelation, Q, Count, F
from django.db.models import Case, IntegerField, Value, When


class Level2:

    def __init__(self, user, candidates):
        self.user = user
        # candidates after level 1
        self.candidates = candidates

    def search(self):
        self.aboutyou_hobbies()
        self.aboutyou_music_types()
        self.aboutyou_foods()
        self.aboutyou_genres()
        self.aboutyou_films()
        self.aboutyou_books()
        self.aboutyou_questionary()
        self.aboutme_hobbies()
        self.aboutme_music_types()
        self.aboutme_foods()
        self.aboutme_genres()
        self.aboutme_films()
        self.aboutme_books()
        self.aboutme_questionary()
        return self.candidates

    def aboutyou_books(self):
        # add annotate count_similar_books field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_you_similar_books=Count('aboutme__books',
                                          filter=Q(aboutme__books__in=self.user.aboutyou.books.all()), distinct=True)
        )

    def aboutyou_films(self):
        # add annotate count_similar_films field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_you_similar_films=Count('aboutme__films',
                                          filter=Q(aboutme__films__in=self.user.aboutyou.films.all()), distinct=True)
        )

    def aboutyou_genres(self):
        # add annotate count_similar_genres field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_you_similar_genres=Count('aboutme__genres',
                                           filter=Q(aboutme__genres__in=self.user.aboutyou.genres.all()), distinct=True)
        )

    def aboutyou_foods(self):
        # add annotate count_similar_foods field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_you_similar_foods=Count('aboutme__foods',
                                          filter=Q(aboutme__foods__in=self.user.aboutyou.foods.all()), distinct=True)
        )

    def aboutyou_music_types(self):
        # add annotate count_similar_music_types field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_you_similar_music_types=Count('aboutme__music_types',
                                                filter=Q(aboutme__music_types__in=self.user.aboutyou.music_types.all()),
                                                distinct=True)
        )

    def aboutyou_hobbies(self):
        # add annotate count_similar_hobbies field (number) for count of similar
        # if you have some bag or error try this:
        # self.candidates = self.candidates.all().annotate(
        self.candidates = self.candidates.annotate(
            count_you_similar_hobbies=Count('aboutme__hobbies',
                                            filter=Q(aboutme__hobbies__in=self.user.aboutyou.hobbies.all()),
                                            distinct=True)
        )

    def aboutyou_questionary(self):
        # get AboutYou model for search all answers in Questionary model
        obj_type = ContentType.objects.get_for_model(AboutYou)
        answers = Answer.objects.filter(
            pk__in=Questionary.objects.filter(user=self.user, content_type=obj_type).values('answer'))
        # add annotate count_similar_questionary field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_you_similar_questionary=Count('questionary__pk', filter=Q(questionary__answer__in=answers),
                                                distinct=True))

    def aboutme_books(self):
        # add annotate count_similar_books field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_me_similar_books=Count('aboutyou__books',
                                          filter=Q(aboutyou__books__in=self.user.aboutme.books.all()), distinct=True)
        )

    def aboutme_films(self):
        # add annotate count_similar_films field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_me_similar_films=Count('aboutyou__films',
                                          filter=Q(aboutyou__films__in=self.user.aboutme.films.all()), distinct=True)
        )

    def aboutme_genres(self):
        # add annotate count_similar_genres field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_me_similar_genres=Count('aboutyou__genres',
                                           filter=Q(aboutyou__genres__in=self.user.aboutme.genres.all()), distinct=True)
        )

    def aboutme_foods(self):
        # add annotate count_similar_foods field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_me_similar_foods=Count('aboutyou__foods',
                                          filter=Q(aboutyou__foods__in=self.user.aboutme.foods.all()), distinct=True)
        )

    def aboutme_music_types(self):
        # add annotate count_similar_music_types field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_me_similar_music_types=Count('aboutyou__music_types',
                                                filter=Q(aboutyou__music_types__in=self.user.aboutme.music_types.all()),
                                                distinct=True)
        )

    def aboutme_hobbies(self):
        # add annotate count_similar_hobbies field (number) for count of similar
        # if you have some bag or error try this:
        # self.candidates = self.candidates.all().annotate(
        self.candidates = self.candidates.annotate(
            count_me_similar_hobbies=Count('aboutyou__hobbies',
                                            filter=Q(aboutyou__hobbies__in=self.user.aboutme.hobbies.all()),
                                            distinct=True)
        )

    def aboutme_questionary(self):
        # get AboutYou model for search all answers in Questionary model
        #FIX.... filter AboutYou and AdoutMe
        obj_type = ContentType.objects.get_for_model(AboutMe)
        answers = Answer.objects.filter(
            pk__in=Questionary.objects.filter(user=self.user, content_type=obj_type).values('answer'))
        # add annotate count_similar_questionary field (number) for count of similar
        self.candidates = self.candidates.annotate(
            count_me_similar_questionary=Count('questionary__pk', filter=Q(questionary__answer__in=answers),
                                                distinct=True))
