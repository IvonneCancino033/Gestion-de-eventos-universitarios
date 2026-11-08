from django.shortcuts import render
from django.db.models import Q

from django.http import HttpResponse
from ...models import Inscripcion


def buscar_participante(request):

    busqueda = request.GET.get('q', '').strip() #lo que me envia el formulario

    inscripciones = Inscripcion.objects.none()

    #busca por nombres
    if busqueda:

        inscripciones = Inscripcion.objects.filter(
            Q(usuario__username__icontains=busqueda)
        ).select_related('usuario','evento')

    return render(
        request,
        'asistencia/buscar_participante.html',
        {
            'inscripciones': inscripciones,
            'busqueda': busqueda
        }
    )

