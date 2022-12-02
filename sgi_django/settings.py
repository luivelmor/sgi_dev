import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8%g(0fkl1=y7233-oia59q)fhu2oolp+nz(6%0!_9xl&i)+tn)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.1.21.24',
    'sgi'
]


# Application definition
INSTALLED_APPS = [
    # My apps
    'inventory.apps.InventoryConfig',
    'gorilla.apps.GorillaConfig',
    # Aux
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'ckeditor',
    'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
    '10.1.21.24',
    '10.1.21.22',
    '150.214.135.171'
]

# debug_toolbar moved here.
if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    # this is the main reason for not showing up the toolbar
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

ROOT_URLCONF = 'sgi_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'sgi_django.wsgi.application'

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'sgi_django',
#        'USER': 'root',
#        'PASSWORD': 'm1_dj4ngu1t0_db',
#        'HOST': 'localhost',
#        'PORT': '3306',
#    }
# }

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sgi_django',
        'USER': 'postgres',
        'PASSWORD': 'm1_dj4ngu1t0_db',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

CKEDITOR_CONFIGS = {
    'default': {
        'height': 150,
    },
}

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
]
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Medias files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Inventory Variables
IMAGES_THUMBNAIL_SIZE = '150px'
MODEL_IMAGES_PATH = 'inventory/deviceModel_images'
MODEL_FILES_PATH = 'inventory/deviceModel_files'
INVOICE_FILES_PATH = 'inventory/invoice_files'
DRIVER_FILES_PATH = 'inventory/driverFile_files'
MODIFICATION_REQUEST_IMAGES_PATH = 'inventory/modificationRequest_images'
MODIFICATION_REQUEST_FILES_PATH = 'inventory/modificationRequest_files'
IMAGES_FILES_PATH = 'images'
TESTING_FILES_PATH = 'testing/files'
# Gorilla Variables
DRIVERS_FILES_PATH = 'gorilla/driver_files'
