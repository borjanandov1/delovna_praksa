from modeltranslation.translator import TranslationOptions, register

from .models import FAQ, OpeningHours, SiteSettings, Testimonial


@register(SiteSettings)
class SiteSettingsTR(TranslationOptions):
    fields = ("tagline", "short_about", "street", "city")


@register(Testimonial)
class TestimonialTR(TranslationOptions):
    fields = ("author", "role", "text")


@register(FAQ)
class FAQTR(TranslationOptions):
    fields = ("question", "answer")


@register(OpeningHours)
class OpeningHoursTR(TranslationOptions):
    fields = ()
