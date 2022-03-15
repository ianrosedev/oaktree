from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "projects/project.html"
    context_object_name = "project"


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    template_name = "projects/project_form.html"
    fields = (
        "title",
        "lead",
        "main_image",
        "body",
        "web_link",
        "github_link",
        "meta_description",
        "is_published",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    template_name = "projects/project_form.html"
    fields = (
        "title",
        "lead",
        "main_image",
        "body",
        "web_link",
        "github_link",
        "meta_description",
        "is_published",
    )


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "projects/project_delete.html"
    context_object_name = "project"
    success_url = reverse_lazy("home")
