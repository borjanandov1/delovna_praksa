"""Local development settings."""

from .base import *  # noqa: F401,F403
from .base import BASE_DIR, MEDIA_ROOT, MEDIA_URL  # noqa: F401

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Print emails to the console instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Serve static files straight from disk, unhashed, so edits show up on reload.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
