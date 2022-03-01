from django.urls import reverse_lazy
from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"
    context_object_name = "post"


class PostCreateView(generic.CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ("title", "body", "meta_description", "is_published")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ("title", "body", "meta_description", "is_published")


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("post_list")
