from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    path('', include('core.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
