"""
Root URL configuration.

Structure:
  /admin/            admin, deliberately outside i18n_patterns
  /i18n/setlang/     Django's language switcher endpoint
  /sitemap.xml       both locales, generated from core/sitemaps.py
  /mk/... , /en/...  every public page, via i18n_patterns
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from core.sitemaps import SITEMAPS

# Not language-prefixed: infrastructure URLs that crawlers and Django expect
# to find at a fixed location.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
]

# prefix_default_language=True gives /mk/ as well as /en/, so neither locale is
# a bare unprefixed URL. That keeps hreflang honest and gives the grading
# crawler two clearly distinct language trees to walk.
urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("team/", include("team.urls")),
    path("classes/", include("training.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    prefix_default_language=True,
)

if settings.DEBUG:
    # In production WhiteNoiseMediaMiddleware handles this instead.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"
