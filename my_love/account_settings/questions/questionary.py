from .questions import questions
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

def get_original_questions():
    return questions


def get_original_questions_keys():
    return get_original_questions().keys()


