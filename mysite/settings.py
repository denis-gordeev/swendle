# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pf-@jxtojga)z+4s*uwbgjrq$aep62-thd0q7f&o77xtpka!_m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
# See https://docs.djangoproject.com/en/1.10/ref/settings/
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'taggit',
    'rest_framework',
    'taggit_serializer',
    'django.contrib.sites',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'api.context_processors.menubar'
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# [START dbconfig]
DATABASES = {
    'default': {
        # If you are using Cloud SQL for MySQL rather than PostgreSQL, set
        # 'ENGINE': 'django.db.backends.mysql' instead of the following.
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'swendle',
        'USER': 'swendle',
        'PASSWORD': 'swendle',
    }
}
# In the flexible environment, you connect to CloudSQL using a unix socket.
# Locally, you can use the CloudSQL proxy to proxy a localhost connection
# to the instance
DATABASES['default']['HOST'] = '/cloudsql/swendle-179717:europe-west1:swendle'
if os.getenv('GAE_INSTANCE'):   
    pass
elif os.getenv('SETTINGS_MODE') == 'prod':
    # Running in development, but want to access the Google Cloud SQL instance in production.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '35.195.163.92',
            'NAME': 'swendle',
            'USER': 'swendle',
            'PASSWORD': 'swendle',
        }
    }
else:
    DATABASES['default']['HOST'] = '127.0.0.1'
# [END dbconfig]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# [START staticurl]
# Fill in your cloud bucket and switch which one of the following 2 lines
# is commented to serve static content from GCS
# STATIC_URL = 'http://storage.googleapis.com/swendle/static/'
STATIC_URL = '/static/'
# [END staticurl]

STATIC_ROOT = 'static/'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # 'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    "allauth.account.auth_backends.AuthenticationBackend",
    # 'rest_framework_social_oauth2.backends.DjangoOAuth2',
    # 'social_core.backends.facebook.FacebookAppOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',
)


REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.permissions.POSTOnlyAuthentication',
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

# SOCIAL_AUTH_FACEBOOK_KEY = '1423149184437463'
# SOCIAL_AUTH_FACEBOOK_SECRET = '48f23c99c9f886749bf656a02256fb5f'

# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = { 'fields': 'id, name, email' }

SITE_ID = 1

AUTH_USER_MODEL = 'api.MyUser'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'swendle.backend@gmail.com'
EMAIL_HOST_PASSWORD = 'swendle.development'
EMAIL_PORT = 587

ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_URL = LOGIN_REDIRECT_URL = '/api/auth/login/'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
