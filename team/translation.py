from modeltranslation.translator import TranslationOptions, register

from .models import Specialty, TeamMember


@register(Specialty)
class SpecialtyTR(TranslationOptions):
    fields = ("name",)


@register(TeamMember)
class TeamMemberTR(TranslationOptions):
    fields = ("name", "role", "short_bio", "bio", "certifications")
