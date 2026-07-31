from modeltranslation.translator import TranslationOptions, register

from .models import Service, ServiceCategory, ServiceImage


@register(ServiceCategory)
class ServiceCategoryTR(TranslationOptions):
    fields = ("name",)


@register(Service)
class ServiceTR(TranslationOptions):
    fields = ("title", "short_desc", "full_desc", "what_included")


@register(ServiceImage)
class ServiceImageTR(TranslationOptions):
    fields = ("caption",)
