from django import template
from random import randrange, sample, choice

from django.contrib.contenttypes.models import ContentType

from articles_settings.models import Gallery
from articles_likes.models import Like

register = template.Library()


@register.simple_tag
def who_like_some_of_your_article(user):
    article = get_random_article_whit_likes(user)
    users = article.get_fans()
    user = choice(list(users))
    return user


@register.simple_tag
def you_like_some_one_article(user):
    article = get_random_article_what_user_like(user)
    return article.user


def get_random_article_what_user_like(user):
    obj_type = ContentType.objects.get_for_model(Gallery)
    likes = Like.objects.filter(user=user).filter(content_type=obj_type)
    like = choice(list(likes))
    return Gallery.objects.get(pk=like.object_id)


def get_random_article_whit_likes(user):
    articles = Gallery.objects.filter(user=user).filter(likes__isnull=False)
    article = choice(list(articles))
    return article
