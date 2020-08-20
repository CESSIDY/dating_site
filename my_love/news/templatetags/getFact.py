from django import template
from random import randrange, sample, choice
from articles_settings.models import Gallery
from django.contrib.contenttypes.models import ContentType
from account_settings.models import Questionary

register = template.Library()


@register.simple_tag
def chose_answer(user):
    question = get_random_question_from_questionary(user)
    answer = question.answer.title
    return answer


def get_random_question_from_questionary(user):
    obj = user.aboutme
    obj_type = ContentType.objects.get_for_model(obj)
    questionary = Questionary.objects.filter(answer__isnull=False)
    question = choice(list(questionary))
    return question
