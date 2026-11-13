from django.contrib import admin
from django.urls import path, include

# El proyecto integra el admin, la autenticacion de Django y la pagina de inicio.
urlpatterns = [
    path("admin/", admin.site.urls),
    # rutas de autenticacion
    path("accounts/", include("django.contrib.auth.urls")),
    # Aplicación principal
    path("", include("core.urls")),
]