import datetime
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from django.conf.urls.static import static
from django.conf import settings
import re


def delete_file(path):
    print("DELETE_" + path)
    return True


class AboutCommonInfo(models.Model):
    # object.get_gender_display()
    # object.get_color_hair_display()
    # object.get_color_aye_display()
    DEFAULT_VAL = 1
    GENDER = (
        (1, 'Other'),
        (2, 'Female'),
        (3, 'Mall'),
    )
    COLOR_HAIR = (
        (DEFAULT_VAL, 'Other'),
        (2, 'Brunette'),
        (3, 'Red'),
        (4, 'Brown'),
        (5, 'Anything'),
        (6, 'Blonde'),
    )
    COLOR_AYE = (
        (DEFAULT_VAL, 'Other'),
        (2, 'Blue'),
        (3, 'Brown'),
        (4, 'Gray'),
        (5, 'Green'),
        (6, 'Hazel'),
        (7, 'Amber')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.IntegerField(choices=GENDER, default=1)
    color_hair = MultiSelectField('Color of hair', choices=COLOR_HAIR, null=True)
    color_aye = MultiSelectField('Color of aye', choices=COLOR_AYE, null=True)
    class Meta:
        abstract = True


class MusicType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Films(models.Model):
    name = models.CharField(max_length=300)
    genres = models.ManyToManyField(Genres)

    def __str__(self):
        return self.name


class Books(models.Model):
    name = models.CharField(max_length=300, unique=True)
    genres = models.ManyToManyField(Genres)

    def __str__(self):
        return self.name


class Hobbies(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Foods(models.Model):
    FOOD_TYPES = (
        ('1', 'animal'),
        ('2', 'vegetable'),
        ('3', 'organic'),
    )
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=20, choices=FOOD_TYPES)

    def __str__(self):
        return self.name


class Countries(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_set')
    # tags = models.ManyToManyField(Tags, related_name='gallery_set', blank=True)
    description = models.TextField(max_length=1000)
    tags = TaggableManager()
    path = models.ImageField(upload_to='images/', default='images/default.png')
    name = models.CharField(max_length=200)
    main = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.name)

    @staticmethod
    def image_del(image_pk, user_pk):
        image = Gallery.objects.get(pk=image_pk)
        if image.user.pk == user_pk:
            image.delete()

    def delete(self, *args, **kwargs):
        self.path.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class AboutMe(AboutCommonInfo):
    birthday = models.DateField('Your birthday', null=True)
    name = models.CharField(max_length=100, help_text='100 characters max.', null=True)
    surname = models.CharField(max_length=100, null=True)
    growth = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    genres = models.ManyToManyField(Genres, blank=True, related_name='my_genres_set')
    music_types = models.ManyToManyField(MusicType, blank=True, related_name='my_music_types_set',
                                         verbose_name='Favorite types of music')
    films = models.ManyToManyField(Films, blank=True, related_name='my_films_set', verbose_name='Favorite films')
    books = models.ManyToManyField(Books, blank=True, related_name='my_books_set', verbose_name='Favorite books')
    hobbies = models.ManyToManyField(Hobbies, blank=True, related_name='my_hobbies_set',
                                     verbose_name='Favorite hobbies')
    foods = models.ManyToManyField(Foods, blank=True, related_name='my_foods_set', verbose_name='Favorite foods')
    country = models.ForeignKey(Countries, blank=True, related_name='my_country_set', on_delete=models.DO_NOTHING,
                                verbose_name='Where are you from?', null=True)

    def __str__(self):
        return self.user.username

    def main_photo(self):
        try:
            main = self.user.gallery_set.get(main=True)
        except:
            return settings.MEDIA_URL + settings.DEFAULT_IMAGE

        return main.path.url

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AboutMe.objects.create(user=instance)

    def get_absolute_url(self):
        return reverse("about_me")


class AboutYou(AboutCommonInfo):
    min_age = models.IntegerField('Minimal age', null=True)
    max_age = models.IntegerField('Maximum age', null=True)
    min_growth = models.FloatField('Minimum growth', null=True)
    max_growth = models.FloatField('Maximum growth', null=True)
    min_weight = models.FloatField('Minimum weight', null=True)
    max_weight = models.FloatField('Maximum weight', null=True)
    genres = models.ManyToManyField(Genres, blank=True, related_name='you_genres_set',
                                    verbose_name='What genres should this person love?')
    music_types = models.ManyToManyField(MusicType, blank=True, related_name='you_music_types_set',
                                         verbose_name='What music?'
                                         )
    films = models.ManyToManyField(Films, blank=True, related_name='you_films_set', verbose_name='What films?')
    books = models.ManyToManyField(Books, blank=True, related_name='you_books_set', verbose_name='Favorite books?')
    hobbies = models.ManyToManyField(Hobbies, blank=True, related_name='you_hobbies_set', verbose_name='Hobbies')
    foods = models.ManyToManyField(Foods, blank=True, related_name='you_foods_set', verbose_name='Foods')
    countries = models.ManyToManyField(Countries, related_name='you_countries_set',
                                       verbose_name='Where is this person from?')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AboutYou.objects.create(user=instance)

    def get_absolute_url(self):
        return reverse("about_you")


@receiver(pre_save, sender=Gallery)
def pre_save_main_image(sender, instance, **kwargs):
    if instance.main:
        Gallery.objects.filter(user=instance.user, main=True).update(main=False)

