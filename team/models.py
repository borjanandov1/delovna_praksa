from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Specialty(models.Model):
    name = models.CharField(_("name"), max_length=80)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("specialty")
        verbose_name_plural = _("specialties")

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(_("full name"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True)
    role = models.CharField(_("role"), max_length=120)
    short_bio = models.CharField(_("short bio"), max_length=255, blank=True)
    bio = models.TextField(_("biography"), blank=True)

    photo = models.ImageField(_("photo"), upload_to="team/", blank=True)
    specialties = models.ManyToManyField(
        Specialty, verbose_name=_("specialties"), blank=True, related_name="members"
    )
    certifications = models.TextField(
        _("certifications"), blank=True, help_text=_("One per line.")
    )
    years_experience = models.PositiveSmallIntegerField(
        _("years of experience"), null=True, blank=True
    )

    email = models.EmailField(_("email"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)

    is_active = models.BooleanField(_("active"), default=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = _("team member")
        verbose_name_plural = _("team members")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team:detail", kwargs={"slug": self.slug})

    @property
    def certification_items(self):
        return [line.strip() for line in self.certifications.splitlines() if line.strip()]
