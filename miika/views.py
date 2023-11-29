from django.http import HttpResponse


def index(request):
    return HttpResponse("The Test Page of Miika")
