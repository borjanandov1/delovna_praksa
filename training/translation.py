from modeltranslation.translator import TranslationOptions, register

from .models import ClassSession, GymClass, MembershipPlan


@register(GymClass)
class GymClassTR(TranslationOptions):
    fields = ("title", "short_desc", "full_desc", "benefits")


@register(ClassSession)
class ClassSessionTR(TranslationOptions):
    fields = ("room",)


@register(MembershipPlan)
class MembershipPlanTR(TranslationOptions):
    fields = ("name", "tagline", "period", "features")
