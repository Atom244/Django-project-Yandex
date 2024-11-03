from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

import catalog.models
import homepage.forms

__all__ = []


def home(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method == "GET":
        template = "homepage/echo.html"
        form = homepage.forms.EchoForm()
        context = {
            "form": form,
        }
        return render(request, template, context)

    return HttpResponseNotAllowed(["POST"])


def echo_submit(request):
    if request.method == "POST":
        form = homepage.forms.EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return HttpResponse(
                text,
                content_type="text/plain; charset=utf-8",
                charset="utf-8",
            )

    return HttpResponseNotAllowed(["POST"])
