from django.db import models
from django.contrib.auth.models import User
from .evento import Evento

#inscripcion a evento universitario (relacion entre usuario y evento)
class Inscripcion(models.Model):
    #estado de la inscripcion
    ESTADOS = [
        ('ACTIVA', 'Activa'),
        ('CANCELADA', 'Cancelada'),
    ]

    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVA')

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT, related_name='inscripciones')

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        # Evita que un usuario se inscriba mas de una vez al mismo evento
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nombre}"