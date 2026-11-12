from django.contrib.auth.decorators import login_required
from ...models import Evento
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


@login_required
def principal_staff(request):
#    if not request.user.is_staff:
#        raise PermissionDenied
    if request.user.is_staff:
        eventos = Evento.objects.all()
    else:
        eventos = Evento.objects.filter(organizador = request.user)

    contexto = {
        "eventos": eventos
    }

    return render(
        request,
        "asistencia/pagina_principal_asistencia.html",
        contexto
    )
