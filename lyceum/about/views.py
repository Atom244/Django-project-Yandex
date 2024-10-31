from django.shortcuts import render

__all__ = []


def description(request):
    template = "about/about.html"
    return render(request, template)
