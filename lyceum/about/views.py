from django.http import HttpResponse


def description(request):
    return HttpResponse("<body>О проекте</body>")
