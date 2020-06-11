from django.contrib.auth.models import User
from django.views.generic import ListView
from account_settings.models import Gallery
from django.shortcuts import render


class ArticlesList(ListView):
    paginate_by = 5
    model = Gallery
    context_object_name = 'articles'
    template_name = 'articles/list.html'
    #queryset = Gallery.objects.all().order_by('-pub_date')  # Default: Model.objects.all()

    def get(self, request, *args, **kwargs):
        self.queryset = request.user.get_articles(kwargs["tag"])
        return super().get(request, *args, **kwargs)
