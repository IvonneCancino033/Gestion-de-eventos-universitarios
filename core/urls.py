from django.urls import path
<<<<<<< HEAD

from . import views

urlpatterns = [
   path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/nuevo/', views.crear_evento, name='crear_evento'),
=======
from . import views

urlpatterns = [
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
>>>>>>> feature/categoria
]