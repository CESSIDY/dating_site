from django import template

register = template.Library()


@register.simple_tag
def check_likes(article, user):
    return article.is_fan(user)
