from django.shortcuts import render, get_object_or_404, redirect
from ...models import Asistencia, Evento
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


#@login_required
def mostrar(request, evento_id):

    evento = get_object_or_404(
            Evento,
            id=evento_id
        )

 #   if Evento.organizador != request.user: #si no es organizador del evento no puede entrar
  #          raise PermissionDenied

    asistentes = Asistencia.objects.filter(
        id=evento_id
    )
    contexto = {
        "Asistentes": asistentes
    }
    return render(
        request,
        "asistencia/mostrar_asistencia.html",
        contexto
    )
