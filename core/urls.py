from django.urls import path

from . import views

urlpatterns = [
   path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/nuevo/', views.crear_evento, name='crear_evento'),
]