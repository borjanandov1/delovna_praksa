from .base import *  # noqa: F401,F403
from .base import BASE_DIR, MEDIA_ROOT, MEDIA_URL  # noqa: F401

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Serve CSS/JS straight from static/ and pick up edits without collectstatic or a restart.
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
