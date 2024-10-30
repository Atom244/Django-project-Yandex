from django.shortcuts import render

__all__ = ["description"]


def description(request):
    template = "about/about.html"
    return render(request, template)
