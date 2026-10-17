from django.views.generic import DetailView, ListView, TemplateView

from .models import WEEKDAYS, ClassSession, GymClass, MembershipPlan


class ClassListView(ListView):
    model = GymClass
    template_name = "training/class_list.html"
    context_object_name = "classes"

    def get_queryset(self):
        qs = GymClass.objects.filter(is_active=True).select_related("trainer")
        intensity = self.request.GET.get("intensity")
        self.active_intensity = None
        if intensity in dict(GymClass.INTENSITIES):
            self.active_intensity = intensity
            qs = qs.filter(intensity=intensity)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["intensities"] = GymClass.INTENSITIES
        ctx["active_intensity"] = self.active_intensity
        return ctx


class ClassDetailView(DetailView):
    model = GymClass
    template_name = "training/class_detail.html"
    context_object_name = "gym_class"

    def get_queryset(self):
        return GymClass.objects.filter(is_active=True).select_related("trainer")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["sessions"] = self.object.sessions.all()
        ctx["related"] = (
            GymClass.objects.filter(is_active=True)
            .exclude(pk=self.object.pk)[:3]
        )
        return ctx


class ScheduleView(TemplateView):
    template_name = "training/schedule.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        sessions = (
            ClassSession.objects.select_related("gym_class", "gym_class__trainer")
            .filter(gym_class__is_active=True)
            .order_by("weekday", "start_time")
        )

        by_day = {value: [] for value, _label in WEEKDAYS}
        for session in sessions:
            by_day[session.weekday].append(session)

        ctx["schedule"] = [(label, by_day[value]) for value, label in WEEKDAYS]
        ctx["has_sessions"] = sessions.exists()
        return ctx


class PricingView(TemplateView):
    template_name = "training/pricing.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["plans"] = MembershipPlan.objects.all()
        return ctx
