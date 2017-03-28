# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# override these in local_settings.py for prod
SECRET_KEY = 'b4d9adgej*%yx+(u!4h86!*5o6#%ubb4ctg+#&n8ke-&6%*m_2'
SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'site@lensreview.photography'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'floppyforms',
    'registration',
    'review',
    'user_media',
    'generic_positions',
    'hvad',
    'pure_pagination',

    'haystack',
    #'whoosh',

    'camera',
    'camera_lens',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'lensreview_photography.urls'

WSGI_APPLICATION = 'lensreview_photography.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages'
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'camera/templates'),
    os.path.join(BASE_DIR, 'camera_lens/templates'),
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# registration/user accounts
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'

# reviews
REVIEW_AVOID_MULTIPLE_REVIEWS = True
REVIEW_FORM_CHOICE_WIDGET = 'django.forms.widgets.RadioSelect'

# pagination
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 1,
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
"""
# haystack search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# without this setting, only one of the indexed models returns
# due to some bug with whoosh
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False
"""
# LOCAL SETTINGS
try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e


# now we can do the debug and other checks after importing local_settings
if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
