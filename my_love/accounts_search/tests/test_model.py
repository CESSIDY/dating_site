import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.urls import reverse
from account_settings.models import AboutCommonInfo as commonInfo, Question, Answer, Questionary
from accounts_search.models import Candidates
from background_data.models import Genres, MusicType, Films, Books, Hobbies, Foods, Countries


class CandidatesTestCase(TestCase):

    def setUp(self):
        def save_questionary(user, obj):
            questions = Question.objects.all()
            for question in questions:
                question = Question.objects.get(pk=question.pk)
                answer = Answer.objects.filter(question=question).first()
                obj_type = ContentType.objects.get_for_model(obj)
                questionary_obj, is_created = Questionary.objects.get_or_create(content_type=obj_type,
                                                                                user=user, question=question,
                                                                                defaults={'answer': answer})
                questionary_obj.answer = answer
                questionary_obj.save()

        def update_aboutMe(user_1, user_2, user_3):
            user_1.first_name = 'firstname_1'
            user_2.first_name = 'firstname_2'
            user_3.first_name = 'firstname_3'

            user_1.last_name = 'lastname_1'
            user_2.last_name = 'lastname_2'
            user_3.last_name = 'lastname_3'

            user_1.is_active = True
            user_2.is_active = True
            user_3.is_active = True

            user_1.aboutme.gender = commonInfo.FEMALE  # user_1 == user_2 = 100%
            user_2.aboutme.gender = commonInfo.MALL  # user_2 == user_1 = 100%
            user_3.aboutme.gender = commonInfo.FEMALE  # user_3 = alone

            user_1.aboutme.color_hair = [index[0] for index in list(commonInfo.COLOR_HAIR)]
            user_2.aboutme.color_hair = [index[0] for index in list(commonInfo.COLOR_HAIR)]
            user_3.aboutme.color_hair = [index[0] for index in list(commonInfo.COLOR_HAIR)]

            user_1.aboutme.color_aye = [index[0] for index in list(commonInfo.COLOR_AYE)]
            user_2.aboutme.color_aye = [index[0] for index in list(commonInfo.COLOR_AYE)]
            user_3.aboutme.color_aye = [index[0] for index in list(commonInfo.COLOR_AYE)]

            user_1.aboutme.activate = True
            user_2.aboutme.activate = True
            user_3.aboutme.activate = True

            d1 = datetime.datetime.now() - datetime.timedelta(days=20 * 365)
            d2 = datetime.datetime.now() - datetime.timedelta(days=20 * 365)
            d3 = datetime.datetime.now() - datetime.timedelta(days=60 * 365)
            user_1.aboutme.birthday = d1
            user_2.aboutme.birthday = d2
            user_3.aboutme.birthday = d3

            user_1.aboutme.weight = 70
            user_2.aboutme.weight = 70
            user_3.aboutme.weight = 70

            user_1.aboutme.growth = 170
            user_2.aboutme.growth = 170
            user_3.aboutme.growth = 170

            user_1.aboutme.genres.set(Genres.objects.all())
            user_2.aboutme.genres.set(Genres.objects.all())
            user_3.aboutme.genres.set(Genres.objects.all())

            user_1.aboutme.music_types.set(MusicType.objects.all())
            user_2.aboutme.music_types.set(MusicType.objects.all())
            user_3.aboutme.music_types.set(MusicType.objects.all())

            user_1.aboutme.films.set(Films.objects.all())
            user_2.aboutme.films.set(Films.objects.all())
            user_3.aboutme.films.set(Films.objects.all())

            user_1.aboutme.books.set(Books.objects.all())
            user_2.aboutme.books.set(Books.objects.all())
            user_3.aboutme.books.set(Books.objects.all())

            user_1.aboutme.hobbies.set(Hobbies.objects.all())
            user_2.aboutme.hobbies.set(Hobbies.objects.all())
            user_3.aboutme.hobbies.set(Hobbies.objects.all())

            user_1.aboutme.foods.set(Foods.objects.all())
            user_2.aboutme.foods.set(Foods.objects.all())
            user_3.aboutme.foods.set(Foods.objects.all())

            user_1.aboutme.country = Countries.objects.first()
            user_2.aboutme.country = Countries.objects.first()
            user_3.aboutme.country = Countries.objects.last()  # Alone

            user_1.aboutme.save()
            user_2.aboutme.save()
            user_3.aboutme.save()
            save_questionary(user_1, user_1.aboutme)
            save_questionary(user_2, user_2.aboutme)
            save_questionary(user_3, user_3.aboutme)

        def update_aboutYou(user_1, user_2, user_3):
            user_1.aboutyou.gender = commonInfo.MALL  # user_1 == user_2 = 100%
            user_2.aboutyou.gender = commonInfo.FEMALE  # user_2 == user_1 = 100%
            user_3.aboutyou.gender = commonInfo.FEMALE  # user_3 = alone

            user_1.aboutyou.color_hair = [index[0] for index in list(commonInfo.COLOR_HAIR)]
            user_2.aboutyou.color_hair = [index[0] for index in list(commonInfo.COLOR_HAIR)]
            user_3.aboutyou.color_hair = [index[0] for index in list(commonInfo.COLOR_HAIR)]

            user_1.aboutyou.color_aye = [index[0] for index in list(commonInfo.COLOR_AYE)]
            user_2.aboutyou.color_aye = [index[0] for index in list(commonInfo.COLOR_AYE)]
            user_3.aboutyou.color_aye = [index[0] for index in list(commonInfo.COLOR_AYE)]

            user_1.aboutyou.min_age = 18
            user_1.aboutyou.max_age = 25
            user_2.aboutyou.min_age = 18
            user_2.aboutyou.max_age = 25
            user_3.aboutyou.min_age = 40  # Alone
            user_3.aboutyou.max_age = 60  # Alone

            user_1.aboutyou.min_growth = 150
            user_1.aboutyou.max_growth = 200
            user_2.aboutyou.min_growth = 150
            user_2.aboutyou.max_growth = 200
            user_3.aboutyou.min_growth = 150
            user_3.aboutyou.max_growth = 200

            user_1.aboutyou.min_weight = 55
            user_1.aboutyou.max_weight = 80
            user_2.aboutyou.min_weight = 55
            user_2.aboutyou.max_weight = 80
            user_3.aboutyou.min_weight = 55
            user_3.aboutyou.max_weight = 80

            user_1.aboutyou.genres.set(Genres.objects.all())
            user_2.aboutyou.genres.set(Genres.objects.all())
            user_3.aboutyou.genres.set(Genres.objects.all())

            user_1.aboutyou.music_types.set(MusicType.objects.all())
            user_2.aboutyou.music_types.set(MusicType.objects.all())
            user_3.aboutyou.music_types.set(MusicType.objects.all())

            user_1.aboutyou.films.set(Films.objects.all())
            user_2.aboutyou.films.set(Films.objects.all())
            user_3.aboutyou.films.set(Films.objects.all())

            user_1.aboutyou.books.set(Books.objects.all())
            user_2.aboutyou.books.set(Books.objects.all())
            user_3.aboutyou.books.set(Books.objects.all())

            user_1.aboutyou.hobbies.set(Hobbies.objects.all())
            user_2.aboutyou.hobbies.set(Hobbies.objects.all())
            user_3.aboutyou.hobbies.set(Hobbies.objects.all())

            user_1.aboutyou.foods.set(Foods.objects.all())
            user_2.aboutyou.foods.set(Foods.objects.all())
            user_3.aboutyou.foods.set(Foods.objects.all())

            user_1.aboutyou.countries.set(Countries.objects.filter(name__contains='1'))
            user_2.aboutyou.countries.set(Countries.objects.filter(name__contains='1'))
            user_3.aboutyou.countries.set(Countries.objects.filter(name__contains='2'))  # Alone

            user_1.aboutyou.save()
            user_2.aboutyou.save()
            user_3.aboutyou.save()
            save_questionary(user_1, user_1.aboutyou)
            save_questionary(user_2, user_2.aboutyou)
            save_questionary(user_3, user_3.aboutyou)

        question = Question.objects.create(me_title='what answer?', you_title='what answer?')
        Answer.objects.create(title='answer_1', question=question)
        Answer.objects.create(title='answer_2', question=question)
        Answer.objects.create(title='answer_3', question=question)
        Genres.objects.create(name='genre_1')
        MusicType.objects.create(name='type_1')
        Films.objects.create(name='film_1')
        Books.objects.create(name='book_1')
        Hobbies.objects.create(name='hobbies_1')
        Foods.objects.create(name='food_1', type=Foods.FOOD_TYPES[0][0])
        Countries.objects.create(name='country_1')
        Countries.objects.create(name='country_2')

        self.user1 = User.objects.create_user('user_1', 'user_1@gmail.com', 'Qwerty1!')  # user_1 == user_2 = 100%
        self.user2 = User.objects.create_user('user_2', 'user_2@gmail.com', 'Qwerty2!')  # user_2 == user_1 = 100%
        self.user3 = User.objects.create_user('user_3', 'user_3@gmail.com', 'Qwerty3!')  # Alone
        self.user1.set_password('Qwerty1!')
        self.user2.set_password('Qwerty1!')
        self.user3.set_password('Qwerty1!')
        update_aboutMe(self.user1, self.user2, self.user3)
        update_aboutYou(self.user1, self.user2, self.user3)
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.client = Client()
        logged_in = self.client.login(username='user_1', password='Qwerty1!')
        self.partner_search = reverse('partners_search')
        self.user1.search_candidates()
        self.user2.search_candidates()

    def test_candidates_search(self):
        # self.client.get(self.partner_search)
        candidates = Candidates.objects.filter(creator=self.user1)
        candidate = candidates.first()
        self.assertEquals(candidates.count(), 1)
        self.assertEquals(candidate.candidate, self.user2)
        self.assertEquals(candidate.common_percentage, 100)

    def test_get_followers(self):
        followers = self.user1.get_followers()
        self.assertEquals(followers.filter(candidate=self.user1).count(), 1)

    def test_remove_candidate(self):
        self.user1.remove_candidate(self.user2.pk)
        candidates_count = self.user1.get_candidates().count()
        self.assertEquals(candidates_count, 0)

