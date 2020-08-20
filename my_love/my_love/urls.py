"""my_love URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from .views import (
    home
)

urlpatterns = [
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
]
if settings.DEBUG:  # new
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#                     static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)