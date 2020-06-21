import datetime
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf.urls.static import static
from django.conf import settings
from PIL import Image
from background_data.models import Genres, MusicType, Films, Foods, Countries, Books, Hobbies
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Abstract model with common fields for models AboutMe, AboutYou
class AboutCommonInfo(models.Model):
    # object.get_gender_display()
    # object.get_color_hair_display()
    # object.get_color_aye_display()
    DEFAULT_VAL = 1
    FEMALE = 2
    MALL = 3
    GENDER = (
        (DEFAULT_VAL, 'Other'),
        (FEMALE, 'Female'),
        (MALL, 'Mall'),
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


# Model for store a users articles
class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_set')
    description = models.TextField(max_length=1000)
    tags = TaggableManager()
    path = models.ImageField(upload_to='images/', default='images/default.png')
    name = models.CharField(max_length=200)
    main = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.name)

    # Check if there is an image on the server if not then return the path to the standard image
    def image(self):
        try:
            if not Image.open(self.path):
                return settings.MEDIA_URL + settings.DEFAULT_IMAGE
            else:
                return self.path.url
        except:
            return settings.MEDIA_URL + settings.DEFAULT_IMAGE

    @staticmethod
    # checks whether the field passed as an argument (user_pk) matches the field of the article owner, if so, it will be deleted
    def image_del(image_pk, user_pk):
        image = Gallery.objects.get(pk=image_pk)
        if image.user.pk == user_pk:
            image.delete()

    # before deleting the article from the database, the image was first deleted from the server
    def delete(self, *args, **kwargs):
        try:
            self.path.delete()
        except:
            pass
        super().delete(*args, **kwargs)

    # before saving the article to the database, the image will be compressed
    def save(self, *args, **kwargs):
        if not self.pk:
            self.path = self.compressImage(self.path)
        super().save(*args, **kwargs)

    # image compress logic
    def compressImage(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        # imageTemproary = imageTemproary.resize((300, 350))
        imageTemproary.save(outputIoStream, format=imageTemproary.format, quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


@receiver(pre_save, sender=Gallery)
# logic to change the main article to the current one
def pre_save_main_image(sender, instance, **kwargs):
    try:
        if instance.main:
            Gallery.objects.filter(user=instance.user, main=True).update(main=False)
    except:
        pass


# a model for storing key information about yourself that will be used to find partners
class AboutMe(AboutCommonInfo):
    activate = models.BooleanField('Activate in search?', default=False)
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

    # get image from main article
    def main_photo(self):
        try:
            main = self.user.gallery_set.get(main=True)
        except:
            return settings.MEDIA_URL + settings.DEFAULT_IMAGE

        return main.path.url

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        # before creating a new user, a AboutMe model will be created
        if created:
            AboutMe.objects.create(user=instance)

    def get_absolute_url(self):
        return reverse("about_me")


# model to store key information about your future partner, this information will also be used to search
class AboutYou(AboutCommonInfo):
    last_search_date = models.DateTimeField(auto_now=True)
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
        # before creating a new user, a AboutYou model will be created
        if created:
            AboutYou.objects.create(user=instance)

    def get_absolute_url(self):
        return reverse("about_you")
