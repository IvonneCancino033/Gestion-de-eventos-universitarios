from django.contrib import admin
from django.urls import include, path

# El proyecto integra el admin, la autenticación de Django y la página de inicio.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("", include('core.asistencia.urls')),
]
