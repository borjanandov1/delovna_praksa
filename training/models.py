from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

WEEKDAYS = [
    (0, _("Monday")),
    (1, _("Tuesday")),
    (2, _("Wednesday")),
    (3, _("Thursday")),
    (4, _("Friday")),
    (5, _("Saturday")),
    (6, _("Sunday")),
]


class GymClass(models.Model):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    INTENSITIES = [
        (LOW, _("Low")),
        (MEDIUM, _("Medium")),
        (HIGH, _("High")),
    ]

    title = models.CharField(_("title"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=140, unique=True)
    short_desc = models.CharField(_("short description"), max_length=255)
    full_desc = models.TextField(_("full description"))
    benefits = models.TextField(_("benefits"), blank=True, help_text=_("One per line."))

    image = models.ImageField(_("image"), upload_to="classes/", blank=True)
    intensity = models.CharField(
        _("intensity"), max_length=10, choices=INTENSITIES, default=MEDIUM
    )
    duration_min = models.PositiveIntegerField(_("duration (minutes)"), default=60)
    capacity = models.PositiveIntegerField(_("capacity"), default=15)
    trainer = models.ForeignKey(
        "team.TeamMember",
        verbose_name=_("trainer"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes",
    )

    is_active = models.BooleanField(_("active"), default=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = _("class")
        verbose_name_plural = _("classes")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("training:class_detail", kwargs={"slug": self.slug})

    @property
    def benefit_items(self):
        return [line.strip() for line in self.benefits.splitlines() if line.strip()]

    @property
    def intensity_badge(self):
        return {self.LOW: "success", self.MEDIUM: "warning", self.HIGH: "danger"}[
            self.intensity
        ]


class ClassSession(models.Model):
    gym_class = models.ForeignKey(
        GymClass,
        verbose_name=_("class"),
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    weekday = models.IntegerField(_("weekday"), choices=WEEKDAYS)
    start_time = models.TimeField(_("start time"))
    room = models.CharField(_("room"), max_length=60, blank=True)

    class Meta:
        ordering = ["weekday", "start_time"]
        unique_together = [("gym_class", "weekday", "start_time")]
        verbose_name = _("class session")
        verbose_name_plural = _("class sessions")

    def __str__(self):
        return f"{self.gym_class.title} — {self.get_weekday_display()} {self.start_time:%H:%M}"

    @property
    def end_time(self):
        from datetime import datetime, timedelta

        base = datetime.combine(datetime.today(), self.start_time)
        return (base + timedelta(minutes=self.gym_class.duration_min)).time()


class MembershipPlan(models.Model):
    name = models.CharField(_("name"), max_length=80)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    tagline = models.CharField(_("tagline"), max_length=160, blank=True)
    price = models.DecimalField(_("price (MKD)"), max_digits=8, decimal_places=0)
    period = models.CharField(_("period"), max_length=40)
    features = models.TextField(_("features"), help_text=_("One per line."))
    is_featured = models.BooleanField(_("highlight this plan"), default=False)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "price"]
        verbose_name = _("membership plan")
        verbose_name_plural = _("membership plans")

    def __str__(self):
        return f"{self.name} — {self.price} MKD"

    @property
    def feature_items(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]
