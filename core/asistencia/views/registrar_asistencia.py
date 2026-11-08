from django.http import HttpResponse



def registrar_asistencia(request, inscripcion_id):
    return HttpResponse(f"Inscripcion seleccionada: {inscripcion_id}")