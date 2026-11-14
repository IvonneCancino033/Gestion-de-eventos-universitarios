from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .categoria import Categoria

#evento universitario
class Evento(models.Model):
    # opciones de estados del evento
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('CERRADO', 'Cerrado'),
        ('CANCELADO', 'Cancelado'),
        ('REAGENDADO', 'Reagendado'),
    ]
    # opciones de recintos del campus
    LUGARES = [
        ('AUDITORIO_PRINCIPAL', 'Auditorio Principal'),
        ('AULA_MAGNA', 'Aula Magna'),
        ('CANCHA_1', 'Cancha 1'),
        ('GIMNASIO', 'Gimnasio'),
        ('LAB_BIOINFORMATICA', 'Laboratorio de Bioinformática'),
        ('SALA_CONFERENCIAS', 'Sala de Conferencias'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    
    fecha_inicio = models.DateTimeField() #cuando inicia el evento (fecha y hora)
    fecha_fin = models.DateTimeField() #cuando termina el evento (fecha y hora)

    lugar = models.CharField(max_length=150, choices=LUGARES)

    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)]) # minimo 1 cupo
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')

    # relaciones ORM
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='eventos')
    organizador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='eventos_creados')

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['fecha_inicio'] #ordena los eventos por fecha de inicio

    def __str__(self):
        return self.nombre
