"""
Which model fields get a per-language copy.

modeltranslation adds real columns (tagline_mk, tagline_en, ...) and swaps the
right one in at read time based on the active language. gettext/.po files only
cover template and Python strings — without this, switching to English would
still show Macedonian services, classes and blog posts.

Every app's translation.py is imported by modeltranslation at startup.
"""

from modeltranslation.translator import TranslationOptions, register

from .models import FAQ, OpeningHours, SiteSettings, Testimonial


@register(SiteSettings)
class SiteSettingsTR(TranslationOptions):
    fields = ("tagline", "short_about", "street", "city")


@register(Testimonial)
class TestimonialTR(TranslationOptions):
    fields = ("role", "text")


@register(FAQ)
class FAQTR(TranslationOptions):
    fields = ("question", "answer")


@register(OpeningHours)
class OpeningHoursTR(TranslationOptions):
    fields = ()
