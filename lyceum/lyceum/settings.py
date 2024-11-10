import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fake_key")

trigger_words = ("", "true", "yes", "1", "y", "t")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG_ENV = os.getenv("DJANGO_DEBUG", "False").lower()
DEBUG = DEBUG_ENV in trigger_words

ALLOW_REVERSE_ENV = os.getenv("DJANGO_ALLOW_REVERSE", "False").lower()
ALLOW_REVERSE = ALLOW_REVERSE_ENV in trigger_words

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1").split(
    " ",
)

INSTALLED_APPS = [
    "users.apps.UsersConfig",
    "feedback.apps.FeedbackConfig",
    "download.apps.DownloadConfig",
    "core.apps.CoreConfig",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "homepage.apps.HomepageConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "django_ckeditor_5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lyceum.middleware.ReverseWordMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "users.middleware.ProxyUserMiddleware",
]

INTERNAL_IPS = []

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "ru-ru"
USE_I18N = True

LANGUAGES = [
    ("ru-ru", _("Russian")),
    ("en-uk", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS += ["127.0.0.1", "localhost"]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

LOGIN_URL = "../login/"

LOGIN_REDIRECT_URL = "../profile/"

LOGOUT_REDIRECT_URL = "../login/"

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "undo",
            "redo",
            "alignment:left",
            "alignment:center",
            "alignment:right",
            "fontColor",
        ],
        "fontColor": {
            "colors": [
                {
                    "color": "rgb(0, 0, 0)",
                    "label": "Black",
                },
            ],
        },
        "height": 300,
        "width": "100%",
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"

EMAIL_ADDRESS = os.getenv("DJANGO_MAIL", "1@examplemail.com")
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

DEFAULT_USER_IS_ACTIVE = os.getenv(
    "DJANGO_DEFAULT_USER_IS_ACTIVE",
    str(DEBUG),
) in [
    "true",
    "True",
    "yes",
    "YES",
    "1",
    "y",
]
