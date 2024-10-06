from django.http import HttpResponse


def index(request):
    return HttpResponse("<body>Hello, world</body>")
