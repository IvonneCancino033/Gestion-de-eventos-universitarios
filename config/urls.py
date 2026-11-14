from django.contrib import admin
from django.urls import path, include

# El proyecto integra el admin, la autenticacion de Django y la pagina de inicio.
urlpatterns = [
    path("admin/", admin.site.urls),
    # rutas de autenticacion (login, logout, recuperar contraseña)
    path("accounts/", include("django.contrib.auth.urls")),
    # gestion de usuarios
    path("usuarios/", include("usuarios.urls")),
    # Aplicación principal
    path("", include("core.urls")),
]
