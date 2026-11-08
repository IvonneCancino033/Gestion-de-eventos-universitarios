from django.urls import path
from .views.asistencia_views import buscar_participante

urlpatterns = [
    path(
        'registrar_asistencia',
        buscar_participante,
        name='buscar_participante'
    ),
]