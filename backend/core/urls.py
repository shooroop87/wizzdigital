from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services_detail, name='services_detail'),
    path('financial-consulting/', views.financial_consulting, name='financial_consulting'),
    path('book-consultation/', views.book_consultation, name='book_consultation'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]