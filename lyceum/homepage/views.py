from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

import catalog.models
import homepage.forms

__all__ = []

from django.views import View

from django.views.generic import FormView, ListView, TemplateView

from homepage import forms


class HomeView(ListView):
    template_name = "homepage/main.html"
    queryset = catalog.models.Item.objects.on_main()
    context_object_name = "items"


class CoffeeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.coffee_count += 1
            profile.save()

        return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


class EchoView(FormView):
    template_name = "homepage/echo.html"
    form_class = forms.EchoForm


class EchoSubmitView(View):
    def post(self, request, *args, **kwargs):
        form = forms.EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return HttpResponse(
                text.encode("utf-8"),
                content_type="text/plain; charset=utf-8",
            )

        return HttpResponse(status=HTTPStatus.UNPROCESSABLE_ENTITY.value)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
