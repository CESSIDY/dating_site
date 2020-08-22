import os
from django.conf import settings
from random import randrange, sample, choice
from django.template.loader import render_to_string
from django.template.response import TemplateResponse


class News:
    def __init__(self, user):
        self.user = user

    def generate(self):
        #t = TemplateResponse(self.request, self.get_random_template(), {})
        #t.render()
        #print(t.content)
        rendered = render_to_string(self.get_random_template(), {'user': self.user})
        return rendered

    def get_random_template(self):
        return choice(list(self.get_templates()))

    @staticmethod
    def get_templates():
        files = os.listdir(settings.PATH_TO_GENERATIVE_TEMPLATES)
        templates = filter(lambda x: x.endswith('.html'), files)
        return templates
