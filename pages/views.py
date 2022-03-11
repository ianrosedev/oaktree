from django.urls import reverse_lazy
from django.views import generic
from blog.models import Post
from .forms import ContactForm


class HomePageView(generic.TemplateView):
    template_name = "pages/home.html"
    extra_context = {"posts": Post.objects.filter(is_published=True)[:4]}


class ContactPageView(generic.FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
