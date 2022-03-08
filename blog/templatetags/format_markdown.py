from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


@register.filter
def format_markdown(text):
    """Change markdown to HTML marked as safe."""
    return mark_safe(markdownify(text))
