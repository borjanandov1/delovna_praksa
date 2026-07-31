from django.views.generic import DetailView, ListView

from .models import TeamMember


class TeamListView(ListView):
    model = TeamMember
    template_name = "team/team_list.html"
    context_object_name = "members"

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True).prefetch_related("specialties")


class TeamDetailView(DetailView):
    model = TeamMember
    template_name = "team/team_detail.html"
    context_object_name = "member"

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True).prefetch_related(
            "specialties", "classes", "posts"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["others"] = (
            TeamMember.objects.filter(is_active=True).exclude(pk=self.object.pk)[:3]
        )
        return ctx
