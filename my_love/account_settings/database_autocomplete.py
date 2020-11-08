from datetime import datetime
from random import randrange, sample, choice

from articles_likes.services import *
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from articles_settings.models import Gallery
from background_data.models import Genres, MusicType, Films, Books, Hobbies, Foods, Countries
from dateutil.relativedelta import relativedelta
from account_settings.models import AboutCommonInfo as commonInfo, Question, Answer, Questionary, AboutMe
from django.db import models
from random import randrange
from datetime import timedelta
from mimesis import Person
from mimesis.enums import Gender
from mimesis import Generic
from django.contrib.auth.models import User
from account_settings import models


class Users:

    def __init__(self):
        self.person = Person('en')
        self.generic = Generic('en')
        self.questions = Question.objects.all()

    def generate(self):
        for i in range(1, 101):
            if i % 2 != 0:
                user_gender = Gender.MALE
            else:
                user_gender = Gender.FEMALE
            firstname = self.person.first_name(gender=user_gender)
            lastname = self.person.last_name(gender=user_gender)
            user = User.objects.create_user(self.person.username(), self.person.email(), 'Qwerty1!')
            user.first_name = firstname
            user.last_name = lastname
            user.is_active = True
            self.update_aboutMe(user)
            self.update_aboutYou(user)
            user.save()

    def update_aboutMe(self, user):
        user.aboutme.gender = choice(list(commonInfo.GENDER))[0]

        randColorHairCount = randrange(1, len(commonInfo.COLOR_HAIR))
        user.aboutme.color_hair = sample([index[0] for index in list(commonInfo.COLOR_HAIR)], k=randColorHairCount)

        randColorAyeCount = randrange(1, len(commonInfo.COLOR_AYE))
        user.aboutme.color_aye = sample([index[0] for index in list(commonInfo.COLOR_AYE)], k=randColorAyeCount)

        user.aboutme.activate = True

        d1 = datetime.strptime('1/1/1970', '%m/%d/%Y')
        d2 = datetime.strptime('1/1/2002', '%m/%d/%Y')
        user.aboutme.birthday = self.random_date(d1, d2).strftime('%Y-%m-%d')

        user.aboutme.weight = randrange(45, 150)
        user.aboutme.growth = randrange(100, 250)

        user.aboutme.genres.set(self.get_random_list_of_multiple_data_from_objects(Genres.objects))
        user.aboutme.music_types.set(self.get_random_list_of_multiple_data_from_objects(MusicType.objects))
        user.aboutme.films.set(self.get_random_list_of_multiple_data_from_objects(Films.objects))
        user.aboutme.books.set(self.get_random_list_of_multiple_data_from_objects(Books.objects))
        user.aboutme.hobbies.set(self.get_random_list_of_multiple_data_from_objects(Hobbies.objects))
        user.aboutme.foods.set(self.get_random_list_of_multiple_data_from_objects(Foods.objects))
        user.aboutme.country = self.get_random_data_from_objects(Countries.objects)
        user.aboutme.save()
        self.save_questionary(user, user.aboutme)

    def update_aboutYou(self, user):
        user.aboutyou.gender = choice(list(commonInfo.GENDER))[0]

        randColorHairCount = randrange(1, len(commonInfo.COLOR_HAIR))
        user.aboutyou.color_hair = sample([index[0] for index in list(commonInfo.COLOR_HAIR)], k=randColorHairCount)

        randColorAyeCount = randrange(1, len(commonInfo.COLOR_AYE))
        user.aboutyou.color_aye = sample([index[0] for index in list(commonInfo.COLOR_AYE)], k=randColorAyeCount)

        min_age = randrange(18, 60)
        user.aboutyou.min_age = min_age
        user.aboutyou.max_age = randrange(min_age, 61)

        min_growth = randrange(100, 250)
        user.aboutyou.min_growth = min_growth
        user.aboutyou.max_growth = randrange(min_growth, 251)

        min_weight = randrange(45, 150)
        user.aboutyou.min_weight = min_weight
        user.aboutyou.max_weight = randrange(min_weight, 151)

        user.aboutyou.genres.set(self.get_random_list_of_multiple_data_from_objects(Genres.objects))
        user.aboutyou.music_types.set(self.get_random_list_of_multiple_data_from_objects(MusicType.objects))
        user.aboutyou.films.set(self.get_random_list_of_multiple_data_from_objects(Films.objects))
        user.aboutyou.books.set(self.get_random_list_of_multiple_data_from_objects(Books.objects))
        user.aboutyou.hobbies.set(self.get_random_list_of_multiple_data_from_objects(Hobbies.objects))
        user.aboutyou.foods.set(self.get_random_list_of_multiple_data_from_objects(Foods.objects))
        user.aboutyou.countries.set(self.get_random_list_of_multiple_data_from_objects(Countries.objects))
        user.aboutyou.save()
        self.save_questionary(user, user.aboutyou)

    def save_questionary(self, user, obj):
        for question in self.questions:
            question = Question.objects.get(pk=question.pk)
            answer = self.get_random_data_from_objects(Answer.objects.filter(question=question))
            obj_type = ContentType.objects.get_for_model(obj)
            questionary_obj, is_created = Questionary.objects.get_or_create(content_type=obj_type,
                                                                            user=user, question=question,
                                                                            defaults={'answer': answer})
            questionary_obj.answer = answer
            questionary_obj.save()

    def random_date(self, start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def get_random_data_from_objects(self, Objects):
        modelDataIds = Objects.values_list('id', flat=True)
        ChoiceId = choice(list(modelDataIds))
        Data = Objects.get(pk=ChoiceId)
        return Data

    def get_random_list_of_multiple_data_from_objects(self, Objects):
        countOfdata = Objects.count()
        randDataCount = randrange(1, countOfdata + 1)
        modelDataIds = Objects.values_list('id', flat=True)
        listOfRandomDataIds = sample(list(modelDataIds), k=randDataCount)
        multipleData = Objects.filter(id__in=listOfRandomDataIds)
        return multipleData


class Articles:
    def __init__(self):
        self.generic = Generic('en')
        self.loreipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ex leo, pulvinar ac congue eu, cursus vitae ligula. Donec consectetur in felis a lobortis. Vivamus ac sem molestie, aliquet orci sit amet, condimentum magna. Nulla tristique vel nunc nec vehicula. In placerat dolor eget nunc ullamcorper, sed varius risus iaculis. Mauris nec molestie tellus. Proin vestibulum maximus pharetra. Duis maximus elementum nulla, non convallis massa ultricies non.' \
                         'Donec mollis neque quis ex aliquam, quis ullamcorper mi suscipit. Ut scelerisque efficitur eros, vitae auctor erat congue nec. Integer accumsan urna eu mi porta pretium. Duis vitae quam sed ex hendrerit ultricies vitae eu felis. Phasellus lacus libero, ornare non turpis vel, auctor aliquam eros. Maecenas vel vulputate ante, ac molestie arcu. Sed ac mauris egestas, accumsan enim vel, bibendum nunc. Aenean mollis nibh vitae turpis fermentum, a egestas augue dictum. Suspendisse ultricies non leo eget mollis.' \
                         'Sed nec lacus felis. Suspendisse commodo augue nisl, non dapibus eros ultricies at. Nam quis dapibus neque, a maximus tortor. Suspendisse pulvinar purus id tincidunt consectetur. Sed vel mauris at erat blandit eleifend. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus turpis lectus, finibus ac volutpat a, vulputate sit amet tortor.'

    def generate(self):
        users = User.objects.all()
        for user in users:
            for index in range(1, 5):
                article = Gallery.objects.create(user=user, main=False, description=self.loreipsum,
                                                 name='Article Test Generator - {}'.format(index))
                article.tags.add("article", "test", "generate", "make love")
                article.save()


class Likes:
    def __init__(self):
        self.generic = Generic('en')

    def generate(self):
        users = User.objects.all()
        articles = Gallery.objects.all()
        for user in users:
            randArticlesCount = randrange(1, 10)
            listOfRandomArticles = sample(list(articles), k=randArticlesCount)
            for article in listOfRandomArticles:
                if is_fan(article, user):
                    remove_like(article, user)
                else:
                    add_like(article, user)
