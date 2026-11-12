from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("eventos/", views.buscar_eventos, name="buscar_eventos"),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
]
