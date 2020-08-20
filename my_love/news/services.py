import os
from django.conf import settings
from random import randrange, sample, choice
from django.template.response import TemplateResponse


class News:
    def __init__(self, request):
        self.request = request

    def generate(self):
        t = TemplateResponse(self.request, self.get_random_template(), {})
        t.render()
        return t.content

    def get_random_template(self):
        return choice(list(self.get_templates()))

    @staticmethod
    def get_templates():
        files = os.listdir(settings.PATH_TO_GENERATIVE_TEMPLATES)
        templates = filter(lambda x: x.endswith('.html'), files)
        return templates
