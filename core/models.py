from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """
    Singleton holding everything the gym owner should be able to edit without a
    developer: contact details, socials, map position, hero copy.

    Always fetched with SiteSettings.load(); the row is forced to pk=1 so there
    can never be a second one.
    """

    name = models.CharField(_("name"), max_length=100, default="FORGE Fitness Studio")
    tagline = models.CharField(_("tagline"), max_length=200, blank=True)
    short_about = models.TextField(_("short about"), blank=True)

    logo = models.ImageField(_("logo"), upload_to="brand/", blank=True)
    hero_image = models.ImageField(_("hero image"), upload_to="brand/", blank=True)

    street = models.CharField(_("street"), max_length=150, blank=True)
    city = models.CharField(_("city"), max_length=80, default="Скопје")
    postal_code = models.CharField(_("postal code"), max_length=20, blank=True)
    phone = models.CharField(_("phone"), max_length=40, blank=True)
    email = models.EmailField(_("email"), blank=True)

    facebook = models.URLField(_("Facebook"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    youtube = models.URLField(_("YouTube"), blank=True)

    map_lat = models.FloatField(_("map latitude"), default=41.9981)
    map_lng = models.FloatField(_("map longitude"), default=21.4254)

    class Meta:
        verbose_name = _("site settings")
        verbose_name_plural = _("site settings")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # pragma: no cover - guard only
        """Refuse deletion; every template assumes this row exists."""
        return

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def full_address(self):
        parts = [self.street, f"{self.postal_code} {self.city}".strip()]
        return ", ".join(p for p in parts if p)


class OpeningHours(models.Model):
    """One row per weekday. Drives the 'Open now / Closed' badge in the header."""

    DAYS = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]

    weekday = models.IntegerField(_("weekday"), choices=DAYS, unique=True)
    opens = models.TimeField(_("opens"), null=True, blank=True)
    closes = models.TimeField(_("closes"), null=True, blank=True)
    is_closed = models.BooleanField(_("closed all day"), default=False)

    class Meta:
        ordering = ["weekday"]
        verbose_name = _("opening hours")
        verbose_name_plural = _("opening hours")

    def __str__(self):
        if self.is_closed or not self.opens or not self.closes:
            return f"{self.get_weekday_display()}: —"
        return f"{self.get_weekday_display()}: {self.opens:%H:%M}–{self.closes:%H:%M}"


class Testimonial(models.Model):
    author = models.CharField(_("author"), max_length=100)
    role = models.CharField(_("role"), max_length=120, blank=True)
    text = models.TextField(_("text"))
    rating = models.PositiveSmallIntegerField(_("rating"), default=5)
    photo = models.ImageField(_("photo"), upload_to="testimonials/", blank=True)
    is_featured = models.BooleanField(_("featured"), default=False)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("testimonial")
        verbose_name_plural = _("testimonials")

    def __str__(self):
        return f"{self.author} ({self.rating}/5)"

    @property
    def stars(self):
        """Template helper: `{% for _ in t.stars %}` renders one filled star each."""
        return range(self.rating)


class FAQ(models.Model):
    GENERAL = "general"
    MEMBERSHIP = "membership"
    TRAINING = "training"
    CATEGORIES = [
        (GENERAL, _("General")),
        (MEMBERSHIP, _("Membership")),
        (TRAINING, _("Training")),
    ]

    question = models.CharField(_("question"), max_length=255)
    answer = models.TextField(_("answer"))
    category = models.CharField(
        _("category"), max_length=20, choices=CATEGORIES, default=GENERAL
    )
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["category", "order", "id"]
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.question
