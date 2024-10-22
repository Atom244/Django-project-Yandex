from django.shortcuts import render

__all__ = ["description"]


def description(request):
    template = "about/about.html"
    context = {}
    return render(request, template, context)
