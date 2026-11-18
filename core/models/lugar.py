from django.db import models

# Lugar fisico del campus donde se realizan los eventos
class Lugar(models.Model):
    nombre = models.CharField(max_length=150, unique=True)  # no se puede repetir
    estado = models.BooleanField(default=True)  # True = activo, False = desactivado

    creado_en = models.DateTimeField(auto_now_add=True)  # fecha en que se creo
    actualizado_en = models.DateTimeField(auto_now=True)  # fecha de la ultima modificacion

    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ['nombre']  # ordena alfabeticamente

    def __str__(self):
        return self.nombre
