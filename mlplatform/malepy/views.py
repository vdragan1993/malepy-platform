from django.shortcuts import render


def index(request):
    """
    Homepage
    """
    return render(request, 'malepy/index.html')

