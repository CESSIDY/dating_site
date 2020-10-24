from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from .views import (
    home
)

urlpatterns = i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', home, name='home'),
    path('like/', include('articles_likes.urls')),
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),
    path('data/', include('background_data.urls')),
    path('logging/', include('logging_user.urls')),
    path('social-auth/', include('allauth.urls')),
    path('settings/', include('account_settings.urls')),
    path('account/', include('account_show.urls')),
    path('accounts/', include('accounts_search.urls')),
    path('articles/settings/', include('articles_settings.urls')),
    path('articles/', include('articles_show.urls')),
    path('news/', include('news.urls')),
)
if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
