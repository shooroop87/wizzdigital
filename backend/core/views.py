from django.shortcuts import render


def index(request):
    """Homepage"""
    return render(request, 'pages/index.html')


def terms(request):
    """Terms and Conditions"""
    return render(request, 'pages/terms.html')


# Error handlers
def page_not_found(request, exception):
    """404 handler"""
    return render(request, 'pages/404.html', {'path': request.path}, status=404)


def internal_server_error(request, *args, **kwargs):
    """500 handler"""
    return render(request, 'pages/500.html', status=500)