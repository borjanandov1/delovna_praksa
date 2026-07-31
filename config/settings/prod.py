"""
Production settings for the FCSE deployment.

Run with:  DJANGO_SETTINGS_MODULE=config.settings.prod
Requires SECRET_KEY, ALLOWED_HOSTS and DEBUG=False in .env
"""

from .base import *  # noqa: F401,F403
from .base import MIDDLEWARE, env

DEBUG = False

# ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS come from .env — see .env.example.

# Swap the plain WhiteNoise middleware for the variant that also serves media.
MIDDLEWARE = [
    "config.whitenoise_media.WhiteNoiseMediaMiddleware"
    if m == "whitenoise.middleware.WhiteNoiseMiddleware"
    else m
    for m in MIDDLEWARE
]

# Pick up newly uploaded media without a restart. Slightly slower per request,
# but this site serves a handful of visitors and the gym owner uploads photos
# through the admin.
WHITENOISE_AUTOREFRESH = True

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        # Hashed filenames + gzip/brotli. If collectstatic errors on a missing
        # file referenced from CSS, fix the reference rather than downgrading
        # to StaticFilesStorage.
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Security -------------------------------------------------------------
# Set HTTPS_ENABLED=False in .env if FCSE serves the site over plain HTTP,
# otherwise SECURE_SSL_REDIRECT will produce an infinite redirect loop.

HTTPS_ENABLED = env.bool("HTTPS_ENABLED", default=True)

SECURE_SSL_REDIRECT = HTTPS_ENABLED
SESSION_COOKIE_SECURE = HTTPS_ENABLED
CSRF_COOKIE_SECURE = HTTPS_ENABLED
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if HTTPS_ENABLED else None

SECURE_HSTS_SECONDS = 31536000 if HTTPS_ENABLED else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = HTTPS_ENABLED
SECURE_HSTS_PRELOAD = HTTPS_ENABLED
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# --- Email ----------------------------------------------------------------

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)

# --- Logging --------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
