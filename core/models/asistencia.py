from django.db import models
from .inscripcion import Inscripcion

class Asistencia(models.Model):

    class Estado(models.TextChoices):
        PRESENTE = 'P', 'Presente' #Valor almacenado, lo que muestra al usuario
        AUSENTE = 'A', 'Ausente'


    fecha_asistencia = models.DateTimeField(auto_now_add=True)#aiatencia del participante
    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.PRESENTE) #Si participante asistio, solo dos opciones

    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE, related_name='asistencia') #una inscripcion solo puede tener un solo resgistro de asistencia

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"Asistencia: {self.inscripcion.usuario.username} - {self.get_estado_display()}" #Asistencia: juan.perez