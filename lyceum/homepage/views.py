from django.http import HttpResponse


def home(request):
    return HttpResponse("<body>Главная</body>")
