from django.views.generic import DetailView, ListView

from .models import Service, ServiceCategory


class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        qs = Service.objects.select_related("category")
        self.category = None
        slug = self.request.GET.get("category")
        if slug:
            self.category = ServiceCategory.objects.filter(slug=slug).first()
            if self.category:
                qs = qs.filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = ServiceCategory.objects.all()
        ctx["active_category"] = self.category
        return ctx


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return Service.objects.select_related("category").prefetch_related("gallery")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related"] = (
            Service.objects.filter(category=self.object.category)
            .exclude(pk=self.object.pk)[:3]
        )
        return ctx
