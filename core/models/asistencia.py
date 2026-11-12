from django.db import models
from .inscripcion import Inscripcion

class Asistencia(models.Model):

    fecha_asistencia = models.DateTimeField(auto_now_add=True)#aiatencia del participante
    estado = models.BooleanField(default=False) #Si participante asistio, solo dos opciones o null

    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE, related_name='asistencia') #una inscripcion solo puede tener un solo resgistro de asistencia

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        estado = "Presente" if self.estado else "Ausente"
        return f"Asistencia: {self.inscripcion.usuario.username} - {estado}" #Asistencia: juan.perez