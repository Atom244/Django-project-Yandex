from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = "homepage/main.html"
    context = {}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
