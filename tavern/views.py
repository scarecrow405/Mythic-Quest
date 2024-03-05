from django.shortcuts import render


def tavern(request):
    return render(request, "tavern/tavern.html")
