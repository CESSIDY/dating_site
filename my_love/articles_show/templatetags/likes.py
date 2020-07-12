from django import template

register = template.Library()


@register.simple_tag
def check_like_on_article(article, user):
    return article.is_fan(user)
