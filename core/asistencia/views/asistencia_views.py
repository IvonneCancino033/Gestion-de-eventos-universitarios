from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ...models import Inscripcion

@login_required
def buscar_participante(request):

    busqueda = request.GET.get('q', '').strip() #lo que me envia el formulario

    inscripciones = Inscripcion.objects.none()

    #busca por nombres
    if busqueda:

        inscripciones = Inscripcion.objects.filter(
            Q(usuario__username__icontains=busqueda),
            evento__organizador=request.user    
        ).select_related('usuario','evento')

    return render(
        request,
        'asistencia/buscar_participante.html',
        {
            'inscripciones': inscripciones,
            'busqueda': busqueda
        }
    )
