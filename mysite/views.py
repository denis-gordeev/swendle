from django.http import HttpResponse


def null_view(request):
    return HttpResponse(status=200)
