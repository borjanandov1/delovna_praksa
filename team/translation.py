from modeltranslation.translator import TranslationOptions, register

from .models import Specialty, TeamMember


@register(Specialty)
class SpecialtyTR(TranslationOptions):
    fields = ("name",)


@register(TeamMember)
class TeamMemberTR(TranslationOptions):
    # `name` stays untranslated — a person's name is the same in both locales.
    fields = ("role", "short_bio", "bio", "certifications")
