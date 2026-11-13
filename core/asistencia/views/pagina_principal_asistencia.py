from django.contrib.auth.decorators import login_required
from ...models import Evento, Inscripcion
from django.shortcuts import render, redirect


@login_required
def principal_staff(request):
    if request.user.is_staff:
        eventos = Evento.objects.all()

    else:
        es_organizador = Evento.objects.filter(
            organizador=request.user
        ).exists()

        if not es_organizador:
            return redirect('inicio')

        eventos = Evento.objects.filter(
            organizador=request.user
        )
    contexto = {
        "eventos": eventos
    }

    return render(
        request,
        "asistencia/pagina_principal_asistencia.html",
        contexto
    )

@login_required
def principal_usuario(request):
    usuario = request.user
    inscripciones = Inscripcion.objects.filter(
        usuario=usuario
    ).select_related('evento', 'asistencia')



    contexto = {
        "inscripciones": inscripciones,
        "usuario": usuario
    }
   
    return render(
        request,
        "asistencia/principal.html",
        contexto
        )