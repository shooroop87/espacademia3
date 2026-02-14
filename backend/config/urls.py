# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

urlpatterns = [
    path("set-language/", set_language, name="set_language"),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("tinymce/", include("tinymce.urls")),
    path("filer/", include("filer.urls")),
    path('', include('core.urls')),
    path('events/', include('events.urls', namespace='events')),
    path('courses/', include('courses.urls', namespace='courses')),
    # path('teachers/', include('teachers.urls', namespace='teachers')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    if "django_browser_reload" in settings.INSTALLED_APPS:
        urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]