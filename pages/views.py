from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from projects.models import Project
from blog.models import Post
from .forms import ContactForm


class HomePageView(generic.TemplateView):
    template_name = "pages/home.html"
    extra_context = {"posts": Post.objects.filter(is_published=True)[:4]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(is_published=True).only(
            "main_image", "title", "lead", "slug"
        )[:3]
        context["posts"] = Post.objects.filter(is_published=True).only(
            "title", "body", "date_created", "slug"
        )[:4]
        return context


class ContactPageView(SuccessMessageMixin, generic.FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Message sent!"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
