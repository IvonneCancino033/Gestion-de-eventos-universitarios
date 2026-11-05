from django.db import models
from .evento import Evento

class Inscripcion(models.Model): #clase inscripcion
    ESTADOS = [
        ('ACTIVA', 'Activa'),
        ('CANCELADA', 'Cancelada'),
    ]

    fecha_inscripcion = models.DateTimeField(auto_now_add=True) #guarda la fecha en que se inscribe el participante
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVA') #guarda el estado de la inscripcion

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscripciones')

    class Meta: #no puede inscribirse dos veces al mismo evento
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nombre}" #nombre del participante y el evento al que se inscribio