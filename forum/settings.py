"""
    For more information on this file, see
    https://docs.djangoproject.com/en/1.8/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.8/ref/settings/

    Needs some environment strings in the live server.

        LIVE -- To know its in the live server.
        SECRET_KEY -- The secret key to be used.
        RETIRED_PASSWORD -- The password of the retired user.
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get( 'LIVE' ):
    DEBUG = False

else:
    DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'hai'

else:
    SECRET_KEY = os.environ[ 'SECRET_KEY' ]


ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'accounts',
    'forum',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


ROOT_URLCONF = 'forum.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join( BASE_DIR, 'templates' ),
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


WSGI_APPLICATION = 'forum.wsgi.application'


# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join( BASE_DIR, 'db.sqlite3' ),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join( BASE_DIR, 'static_root' )


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join( BASE_DIR, 'static' ),
)


LOGIN_URL = 'accounts:login'
LOGOUT_URL = 'accounts:logout'
LOGIN_REDIRECT_URL = '/'


AUTH_USER_MODEL = 'accounts.Account'


RETIRED_USERNAME = 'user_removed'

if DEBUG:
    RETIRED_PASSWORD = 'a'

else:
    RETIRED_PASSWORD = os.environ[ 'RETIRED_PASSWORD' ]


POSTS_PER_PAGE = 10     # in a thread
THREADS_PER_PAGE = 10   # in a sub-forum


EMOTES = {
    ':@': STATIC_URL + 'emotes/angry.png',
    ':s': STATIC_URL + 'emotes/confused.png',
    ':S': STATIC_URL + 'emotes/confused.png',
    'B)': STATIC_URL + 'emotes/cool.png',
    '>(': STATIC_URL + 'emotes/crying.png',
    ':D': STATIC_URL + 'emotes/glad.png',
    'xD': STATIC_URL + 'emotes/grin.png',
    'O_o': STATIC_URL + 'emotes/O_o.png',
    ':p': STATIC_URL + 'emotes/razz.png',
    ':P': STATIC_URL + 'emotes/razz.png',
    ':(': STATIC_URL + 'emotes/sad.png',
    ':o': STATIC_URL + 'emotes/shame.png',
    ':O': STATIC_URL + 'emotes/shame.png',
    ':)': STATIC_URL + 'emotes/smile.png',
    ':<': STATIC_URL + 'emotes/surprised.png',
    ':/': STATIC_URL + 'emotes/uhm.png',
    ':|': STATIC_URL + 'emotes/unpleased.png',
    ';)': STATIC_URL + 'emotes/wink.png',
}
