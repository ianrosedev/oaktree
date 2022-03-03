from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ("title", "body", "meta_description", "is_published")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ("title", "body", "meta_description", "is_published")


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("post_list")
