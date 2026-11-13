from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login, logout, recuperar contraseña
    path("usuarios/", include("usuarios.urls")),  # gestion de usuarios
    path("", include("core.urls")),
]

