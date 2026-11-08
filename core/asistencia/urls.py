
from django.urls import path

from .views.asistencia_views import buscar_participante
from .views.registrar_asistencia import registrar_asistencia

urlpatterns = [
    path(
        'buscar_participante/',
        buscar_participante,
        name='buscar_participante'
    ),

    path(
        'registrar_asistencia/<int:inscripcion_id>/',
        registrar_asistencia,
        name='registrar_asistencia'
    ),
]