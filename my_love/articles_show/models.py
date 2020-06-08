from django.db.models import Case, BooleanField, Value, When
from django.db import models
from django.contrib.auth.models import User
from account_settings.models import Gallery


def get_articles(self):
    # candidates_creator_sets
    # gallery_set
    candidates = self.get_candidates().values_list('candidate')
    return Gallery.objects.annotate(
        candidate=Case(
            When(user_id__in=candidates, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).order_by('-pub_date')


User.add_to_class("get_articles", get_articles)
