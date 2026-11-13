from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from ...models import Inscripcion, Evento


@login_required
def estadisticas(request, evento_id):

    evento = get_object_or_404(Evento, id=evento_id)

    if evento.organizador != request.user and not request.user.is_superuser:
        raise PermissionDenied

    # Obtener inscripciones activas
    inscripciones = Inscripcion.objects.filter(
        evento=evento,
        estado='ACTIVA'
    ).select_related(
        'usuario',
        'asistencia'
    )

    # agregate permite obtener estadisticas
    estadisticas = inscripciones.aggregate(
        total_inscritos=Count('id'),

        presentes=Count(
            'id',
            filter=Q(asistencia__estado=True)
        ),

        ausentes=Count(
            'id',
            filter=Q(asistencia__estado=False)
        ),


    )

    total = estadisticas['total_inscritos']
    presentes = estadisticas['presentes']

    # Calcular porcentaje
    porcentaje_asistencia = (
        round((presentes / total) * 100, 2)
        if total > 0 else 0
    )

    porcentaje_ausencia = (
        round((estadisticas['ausentes'] / total) * 100, 2)
        if total > 0 else 0
    )

    contexto = {
        'evento': evento,
        'inscripciones': inscripciones,
        'estadisticas': estadisticas,
        'porcentaje_asistencia': porcentaje_asistencia,
        'porcentaje_ausencia': porcentaje_ausencia,
    }

    return render(
        request,
        'asistencia/estadisticas.html',
        contexto
    )