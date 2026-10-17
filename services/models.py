from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ServiceCategory(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=120, unique=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = _("service category")
        verbose_name_plural = _("service categories")

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
    )
    title = models.CharField(_("title"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=170, unique=True)
    icon = models.CharField(
        _("icon"),
        max_length=50,
        default="bi-lightning-charge",
        help_text=_("Bootstrap Icons class, e.g. bi-heart-pulse"),
    )
    short_desc = models.CharField(_("short description"), max_length=255)
    full_desc = models.TextField(_("full description"))
    what_included = models.TextField(
        _("what's included"), blank=True, help_text=_("One item per line.")
    )
    price_from = models.DecimalField(
        _("price from (MKD)"), max_digits=8, decimal_places=0, null=True, blank=True
    )
    duration_min = models.PositiveIntegerField(
        _("duration (minutes)"), null=True, blank=True
    )
    image = models.ImageField(_("image"), upload_to="services/", blank=True)
    is_featured = models.BooleanField(_("featured on homepage"), default=False)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})

    @property
    def included_items(self):
        return [line.strip() for line in self.what_included.splitlines() if line.strip()]


class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service,
        verbose_name=_("service"),
        on_delete=models.CASCADE,
        related_name="gallery",
    )
    image = models.ImageField(_("image"), upload_to="services/gallery/")
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("service image")
        verbose_name_plural = _("service images")

    def __str__(self):
        return f"{self.service.title} — {self.caption or self.pk}"
