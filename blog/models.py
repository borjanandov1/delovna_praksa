from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("name"), max_length=80)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = _("blog category")
        verbose_name_plural = _("blog categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('blog:list')}?category={self.slug}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_published=True, published_at__lte=timezone.now())
        )


class Post(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=220, unique=True)
    excerpt = models.TextField(_("excerpt"), max_length=400)
    body = models.TextField(_("body"))

    cover_image = models.ImageField(_("cover image"), upload_to="blog/", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    author = models.ForeignKey(
        "team.TeamMember",
        verbose_name=_("author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    published_at = models.DateTimeField(_("published at"), default=timezone.now)
    is_published = models.BooleanField(_("published"), default=True)
    views = models.PositiveIntegerField(_("views"), default=0, editable=False)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at"]
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        indexes = [models.Index(fields=["-published_at"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def reading_time(self):
        """Rough minutes-to-read, at ~200 words per minute."""
        return max(1, round(len(self.body.split()) / 200))
