from django.shortcuts import render


def index(request):
    """Home page view"""
    return render(request, 'pages/index.html')


def services_detail(request):
    """Services detail page view"""
    return render(request, 'pages/services_detail.html')


def financial_consulting(request):
    """Financial Consulting page view"""
    return render(request, 'pages/financial_consulting.html')


def book_consultation(request):
    """Book Consultation page view"""
    return render(request, 'pages/book_consultation.html')


def terms(request):
    """Terms and Conditions page view"""
    return render(request, 'pages/terms.html')


def privacy(request):
    """Privacy Policy page view"""
    return render(request, 'pages/privacy.html')


def page_not_found(request, exception):
    """Custom 404 error handler"""
    return render(request, 'pages/404.html', status=404)


def internal_server_error(request):
    """Custom 500 error handler"""
    return render(request, 'pages/500.html', status=500)
