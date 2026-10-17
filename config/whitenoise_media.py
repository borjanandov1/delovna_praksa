from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware


class WhiteNoiseMediaMiddleware(WhiteNoiseMiddleware):
    def __init__(self, get_response=None, settings=settings):
        super().__init__(get_response, settings)
        media_root = getattr(settings, "MEDIA_ROOT", None)
        media_url = getattr(settings, "MEDIA_URL", None)
        if media_root and media_url:
            self.add_files(str(media_root), prefix=media_url)
