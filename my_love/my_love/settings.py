"""
Django settings for my_love project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '74a=5tfq0@ljlw6=^ez)ovmo$kd8o5gb@+kiz1ztcp-2%1vq)w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# '127.0.0.1', '192.168.0.108'
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # app for store and manipulate ancillary data
    'background_data.apps.BackgroundDataConfig',
    # app contains the logic of user logging
    # 'logging_user.apps.LoggingUserConfig',
    # app for manipulation of the user account
    'account_settings.apps.AccountSettingsConfig',
    # app for display user data
    'account_show.apps.AccountShowConfig',
    # app for search of candidates
    'accounts_search.apps.AccountsSearchConfig',
    # app for display articles
    'articles_show.apps.ArticlesShowConfig',
    # app for store and manipulate articles
    'articles_settings.apps.ArticlesSettingsConfig',
    # app to make likes on articles
    'articles_likes.apps.ArticlesLikesConfig',
    # app contains some staff to user social auth
    'accounts_social_auth.apps.AccountsSocialAuthConfig',
    'news.apps.NewsConfig',
    'django.contrib.admin',
    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The app includes Select2 driven Django Widgets.
    'django_select2',
    # The best way to have Django DRY forms. Build programmatic reusable layouts out of components,
    # having full control of the rendered HTML without writing HTML in templates.
    'crispy_forms',
    # A simpler approach to tagging with Django
    'taggit',
    # A new model field and form field. With this you can get a multiple select from a choices.
    # Stores to the database as a CharField of comma-separated values.
    'multiselectfield',
    # The following apps are required:
    'django.contrib.sites',
    'channels',
    # ckeditor
    'ckeditor',
    'ckeditor_uploader',
    # Auth from social
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # include the providers you want to enable:
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_framework'
]

SITE_ID = 1

# EMAIL SEND LOGIC
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_FORMS = {'login': 'accounts_social_auth.forms.MyCustomLoginForm'}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'js_sdk',
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
    },
    'discord': {
        'METHOD': 'js_sdk',
    },
    'telegram': {
        'TOKEN': '1328729898:AAHJGSYMBB4JH_S8QhdkhH-W9TYcxjQ0qes'
    }
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DEBUG_TOOLBAR = DEBUG  # Can override using the debug toolbar here
if DEBUG_TOOLBAR:
    def show_toolbar(request):
        return True


    # This example is unlikely to be appropriate for your project.
    DEBUG_TOOLBAR_CONFIG = {
        # Toolbar options
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': show_toolbar
    }
    INTERNAL_IPS = ['*']
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    # DEBUG SETTINGS:
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

ROOT_URLCONF = 'my_love.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'my_love/templates'),
            os.path.join(BASE_DIR, 'account_settings/templates'),
            os.path.join(BASE_DIR, 'account_show/templates'),
            os.path.join(BASE_DIR, 'accounts_search/templates'),
            os.path.join(BASE_DIR, 'accounts_social_auth/templates'),
            os.path.join(BASE_DIR, 'articles_settings/templates'),
            os.path.join(BASE_DIR, 'articles_show/templates'),
            os.path.join(BASE_DIR, 'background_data/templates'),
            os.path.join(BASE_DIR, 'news/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

PATH_TO_GENERATIVE_TEMPLATES = os.path.join(BASE_DIR, 'news/templates')

WSGI_APPLICATION = 'my_love.wsgi.application'

ASGI_APPLICATION = "my_love.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'make_love_db',
        'USER': 'make_love_admin',
        'PASSWORD': 'makelovepassword',
        'HOST': '127.0.0.1',
        'PORT': '6613',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
]

CKEDITOR_BASEPATH = "/static_root/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "/media/images/"

# ROUTE FOR DEFAULT IMAGE:
DEFAULT_IMAGE = 'images/default.png'
# DEFAULT LOGIN AND LOGOUT URL
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
# crispy_forms SETTINGS:
CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
