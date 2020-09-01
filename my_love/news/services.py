import os
from django.conf import settings
from random import randrange, sample, choice
from django.template.loader import render_to_string
from django.template.response import TemplateResponse


class News:
    def __init__(self, user, lang_code):
        self.user = user
        self.lang_code = lang_code


    def generate(self):
        for index in range(1, 10):
            try:
                template = self.get_random_template()
                rendered = render_to_string(template, {'user': self.user, 'lang_code': self.lang_code})
            except:
                rendered = ''
            if rendered:
                break
        return rendered

    def get_random_template(self):
        return choice(list(self.get_templates()))

    @staticmethod
    def get_templates():
        files = os.listdir(settings.PATH_TO_GENERATIVE_TEMPLATES)
        templates = filter(lambda x: x.endswith('.html'), files)
        return templates
