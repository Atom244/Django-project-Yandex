from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def item_num(request, num):
    return HttpResponse(num)


def item_converter_num(request, number):
    return HttpResponse(number)
