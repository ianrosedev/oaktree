from django.views.generic import TemplateView
from blog.models import Post


class HomePageView(TemplateView):
    template_name = "pages/home.html"
    extra_context = {"posts": Post.objects.filter(is_published=True)[:4]}
