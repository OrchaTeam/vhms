from __future__ import absolute_import, unicode_literals
import dj_database_url

SECRET_KEY = "4b3b840c-16a2-4a06-a772-eac93b8ae12278f84f40-2ee7-4ced-8142-e0b42a20c56a8b98d246-057b-4afa-8c08-2177451fca4f"

USE_SOUTH = True

ADMINS = (
    ("Eugene Belozerov", "belozja@gmail.com"),
    ("Alexander Klimov", "klimov.alexandr@gmail.com"),
    ("Anton Smirnov", "lexussab@gmail.com"),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = ["*"]

TIME_ZONE = "Europe/Moscow"

USE_TZ = True

LANGUAGE_CODE = "en"

# Supported languages
_ = lambda s: s
LANGUAGES = (
    ('en', _('English')),
)

# Global False for Production Server
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

USE_I18N = False

INTERNAL_IPS = ("127.0.0.1",)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

# Backends
AUTHENTICATION_BACKENDS = (
    "apps.profiles.auth_backends.VHMSProfileModelBackend",
    "django.contrib.auth.backends.ModelBackend",
    #"allauth.account.auth_backends.AuthenticationBackend",
    )

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

FILE_UPLOAD_PERMISSIONS = 0o644


#############
# DATABASES #
#############

DATABASES = {
    'default': dj_database_url.config(),
}


#########
# PATHS #
#########

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "assets"),
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../..',  'media')

ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, "fixtures"),
)

ADMIN_MEDIA_PREFIX = 'media/media-admin/'

################
# APPLICATIONS #
################

DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    )

MEZZANINE_APPS = (
    #"mezzanine.boot",
    #"mezzanine.conf",
    #"mezzanine.core",
    #"mezzanine.generic",
    #"mezzanine.forms",
    #"mezzanine.pages",
    #"mezzanine.accounts",
    #"mezzanine.blog",
    #"mezzanine.galleries",
    #"mezzanine.twitter",
    #"mezzanine.mobile",
    )

THIRD_PARTY_APPS = (
    "allauth",
    "allauth.account",
    #"allauth.socialaccount",
    #"allauth.socialaccount.providers.github",
    #"allauth.socialaccount.providers.facebook",
    #"allauth.socialaccount.providers.vk",
    "widget_tweaks",
    "gunicorn",
    "debug_toolbar",
    "storages",
    )

LOCAL_APPS = (
    "apps.core",
    "apps.profiles",
    "apps.utils",
    )

INSTALLED_APPS = DJANGO_APPS + MEZZANINE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    #"mezzanine.conf.context_processors.settings",
    #"mezzanine.pages.context_processors.page",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

MIDDLEWARE_CLASSES = (
    #"mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    #"mezzanine.core.request.CurrentRequestMiddleware",
    #"mezzanine.core.middleware.RedirectFallbackMiddleware",
    #"mezzanine.core.middleware.TemplateForDeviceMiddleware",
    #"mezzanine.core.middleware.TemplateForHostMiddleware",
    #"mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    #"mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    #"mezzanine.pages.middleware.PageMiddleware",
    #"mezzanine.core.middleware.FetchFromCacheMiddleware",
)

PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

try:
    from config.local_settings import *
except ImportError:
    pass

try:
    from config.account_settings import *
except ImportError:
    pass

try:
    from config.profile_settings import *
except ImportError:
    pass

try:
    from config.storages_settings import *
except ImportError:
    pass

try:
    from config.utils_settings import *
except ImportError:
    pass

try:
    from mezzanine.utils.conf import set_dynamic_settings
    set_dynamic_settings(globals())
except ImportError:
    pass

