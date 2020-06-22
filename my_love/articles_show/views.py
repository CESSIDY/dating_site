from django.views.generic import ListView
from articles_settings.models import Gallery

# show list of articles by (tag or all)
class ArticlesList(ListView):
    paginate_by = 5
    model = Gallery
    context_object_name = 'articles'
    template_name = 'articles/list.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        data = self.request.user.get_articles(self.kwargs["tag"])
        return data
