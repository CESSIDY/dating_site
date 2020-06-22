from django.db.models import Case, BooleanField, Value, When
from django.contrib.auth.models import User
from articles_settings.models import Gallery


# User method what returns articles by (tag or all)
def get_articles(self, tag=''):
    # candidates_creator_sets
    # gallery_set
    # Get all candidates for current user
    candidates = self.get_candidates().values_list('candidate')
    # Add annotate candidate field (bool) to display the author of
    # the articles if he is in the current user candidate list
    articles = Gallery.objects.annotate(
        candidate=Case(
            When(user_id__in=candidates, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).order_by('-pub_date')
    # if tag  variable is not empty than star the search
    if tag:
        articles = articles.filter(tags__name__in=[tag])
    return articles


User.add_to_class("get_articles", get_articles)
