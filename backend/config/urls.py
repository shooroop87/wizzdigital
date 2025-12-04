from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server_error'

urlpatterns = [
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)