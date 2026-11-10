from django.shortcuts import render, get_object_or_404, redirect
from ...models import Asistencia, Evento, Inscripcion
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def mostrar(request, evento_id):

    evento = get_object_or_404(
            Evento,
            id=evento_id
        )


    if evento.organizador != request.user: #si no es organizador del evento no puede entrar
        raise PermissionDenied


    inscripciones = Inscripcion.objects.filter(
        evento=evento
    ).select_related('asistencia')

    contexto = {
        "evento": evento,
#        
        "inscripciones": inscripciones   }

    return render(
        request,
        "asistencia/mostrar_asistencia.html",
        contexto
    )

