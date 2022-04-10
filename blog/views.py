from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    extra_context = {"common_tags": Post.tags.most_common(min_count=1)}
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class TagListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_published=True, tags__slug=self.kwargs["tag"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_tag"] = (
            Post.tags.all().filter(slug__exact=self.kwargs["tag"]).first()
        )
        return context


class SearchListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return (
                Post.objects.filter(is_published=True)
                .filter(Q(title__icontains=query) | Q(tags__name__iexact=query))
                .distinct()
            )
        else:
            return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_query"] = self.request.GET.get("q")
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ("title", "body", "meta_description", "tags", "is_published")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ("title", "body", "meta_description", "tags", "is_published")


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("post_list")
