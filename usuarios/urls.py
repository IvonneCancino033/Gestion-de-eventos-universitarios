from django.urls import path

from . import views

app_name = "usuarios"  # para usar {% url 'usuarios:lista' %}

urlpatterns = [
    path("", views.lista_usuarios, name="lista"),
    path("nuevo/", views.crear_usuario, name="crear"),
    path("editar/<int:pk>/", views.editar_usuario, name="editar"),
    path("estado/<int:pk>/", views.cambiar_estado_usuario, name="cambiar_estado"),
]
