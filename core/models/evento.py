from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .categoria import Categoria

class Evento(models.Model): #clase evento
    ESTADOS = [
        ('ACTIVO', 'Disponible'),
        ('EN EJECUCION', 'Cerrado'),
        ('CANCELADO', 'Cancelado'),
        ('REAGENDADO', 'reagendado'),
    ]

    LUGARES = [
        ('AUDITORIO_PRINCIPAL', 'Auditorio Principal'),
        ('AULA_MAGNA', 'Aula Magna'),
        ('CANCHA 1', 'Cancha 1'),
        ('GIMNASIO', 'Gimnasio'),
        ('LAB_BIOINFORMATICA', 'Laboratorio de Bioinformática'),
        ('SALA_CONFERENCIAS', 'Sala de Conferencias'),
    ]

    nombre = models.CharField(max_length=150) #nombre del evento
    descripcion = models.TextField()
    
    fecha_inicio = models.DateField() #cuando inicia el evento
    fecha_fin = models.DateField() #cuando termina el evento

    lugar = models.CharField(max_length=150, choices=LUGARES)

    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)]) #la cantidad de asistentes
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='eventos')
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_creados')

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.nombre