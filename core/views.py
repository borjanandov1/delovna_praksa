from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from blog.models import Post
from services.models import Service
from team.models import TeamMember
from training.models import GymClass, MembershipPlan

from .models import FAQ, Testimonial


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            featured_services=Service.objects.filter(is_featured=True)[:3],
            featured_classes=GymClass.objects.filter(is_active=True)[:4],
            trainers=TeamMember.objects.filter(is_active=True)[:4],
            plans=MembershipPlan.objects.all()[:3],
            testimonials=Testimonial.objects.filter(is_featured=True)[:3],
            latest_posts=Post.published.select_related("category", "author")[:3],
            trainer_count=TeamMember.objects.filter(is_active=True).count(),
            class_count=GymClass.objects.filter(is_active=True).count(),
        )
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["trainers"] = TeamMember.objects.filter(is_active=True)[:4]
        ctx["testimonials"] = Testimonial.objects.all()[:6]
        ctx["milestones"] = [
            (2019, _("Opened with two racks in a converted textile workshop.")),
            (2021, _("Expanded to 600m² and added the group-class studio.")),
            (2023, _("Certified strength & conditioning programme launched.")),
            (2025, _("1200 members and a coaching team of eight.")),
        ]
        return ctx


class FAQView(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        grouped = {}
        for item in FAQ.objects.all():
            grouped.setdefault(item.get_category_display(), []).append(item)
        ctx["faq_groups"] = grouped
        return ctx


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"


class TermsView(TemplateView):
    template_name = "core/terms.html"


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
