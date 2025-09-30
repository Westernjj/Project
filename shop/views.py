from django.http import HttpResponse

def index(request):
    return HttpResponse("Вітаю у розділі магазин – товари!")

