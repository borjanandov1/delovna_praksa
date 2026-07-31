"""
Serve MEDIA_ROOT through WhiteNoise in production.

With DEBUG=False Django stops serving MEDIA_URL, so every admin-uploaded image
(trainer photos, class covers, blog headers) 404s. That is the single most common
"all my images disappeared in production" failure.

If the FCSE deployment puts nginx in front of Django, prefer an nginx `location
/media/` block instead and drop this middleware — nginx serves static files far
more efficiently. This exists so the site is correct even with no web server in
front of it.
"""

from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware


class WhiteNoiseMediaMiddleware(WhiteNoiseMiddleware):
    def __init__(self, get_response=None, settings=settings):
        super().__init__(get_response, settings)
        media_root = getattr(settings, "MEDIA_ROOT", None)
        media_url = getattr(settings, "MEDIA_URL", None)
        if media_root and media_url:
            self.add_files(str(media_root), prefix=media_url)
