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
        if request.user.is_staff:
            inscripciones = Inscripcion.objects.filter(
            Q(usuario__username__icontains=busqueda)    
        ).select_related('usuario','evento')
        
        else:
            inscripciones = Inscripcion.objects.filter(
            Q(usuario__username__icontains=busqueda),
            evento__organizador=request.user    
        ).select_related('usuario','evento')

    
    contexto = {
                'inscripciones': inscripciones,
                'busqueda': busqueda
            }

    return render(
        request,
        'asistencia/buscar_participante.html',
        contexto
    )
