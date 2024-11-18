from django.views.generic import TemplateView

__all__ = []


class AboutView(TemplateView):
    template_name = "about/about.html"

