import datetime
from django.db import models
from django.contrib.auth.models import User


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
