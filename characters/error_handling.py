from django.shortcuts import render


def handle_404(request, exception=None):
    # TODO: ADD 'exception' in the argunemts above
    return render(request, 'errors/404.html', status=404)


def handle_403(request):
    return render(request, 'errors/403.html', status=403)
