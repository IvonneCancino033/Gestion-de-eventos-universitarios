from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ..forms.asistencia_form import AsistenciaForm

from ...models import Inscripcion, Asistencia

@login_required
def registrar_asistencia(request, inscripcion_id):

    inscripcion = get_object_or_404(
        Inscripcion,
        id=inscripcion_id
    )

    
    if inscripcion.evento.organizador != request.user: #si no es organizador del evento no puede registrar asistencia
        raise PermissionDenied

    asistencia, creada = Asistencia.objects.get_or_create(
        inscripcion=inscripcion
    )

    if request.method == 'POST':

        form = AsistenciaForm(request.POST, instance=asistencia)

        if form.is_valid():
            form.save()
            return redirect('buscar_participante')

    else:
        form = AsistenciaForm(instance=asistencia)

    return render(
        request,
        'asistencia/registrar_asistencia.html',
        {
            'form': form,
            'inscripcion': inscripcion
        }
    )
