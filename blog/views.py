from django.db.models import F, Q
from django.views.generic import DetailView, ListView

from .models import Category, Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        qs = Post.published.select_related("category", "author")

        self.active_category = None
        slug = self.request.GET.get("category")
        if slug:
            self.active_category = Category.objects.filter(slug=slug).first()
            if self.active_category:
                qs = qs.filter(category=self.active_category)

        self.query = self.request.GET.get("q", "").strip()
        if self.query:
            qs = qs.filter(
                Q(title__icontains=self.query)
                | Q(excerpt__icontains=self.query)
                | Q(body__icontains=self.query)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["active_category"] = self.active_category
        ctx["query"] = self.query
        return ctx

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["blog/partials/_post_grid.html"]
        return [self.template_name]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.published.select_related("category", "author")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        related = Post.published.exclude(pk=self.object.pk)
        if self.object.category:
            related = related.filter(category=self.object.category)
        ctx["related"] = related[:3]
        return ctx
