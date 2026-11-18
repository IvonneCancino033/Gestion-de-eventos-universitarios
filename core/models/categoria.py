from django.db import models #django para crear la base de datos categoria

#Modelo categoria de eventos universitarios
class Categoria(models.Model): #clase categoria
    nombre = models.CharField(max_length=100, unique=True) #nombre de la categoria
    descripcion = models.TextField(blank=True, null=True) #descripcion del evento
    estado = models.BooleanField(default=True) #indica si la categoria esta activa o inactiva
    
    creado_en = models.DateTimeField(auto_now_add=True) #fecha y hora de la creacion de la categoria
    actualizado_en = models.DateTimeField(auto_now=True) #fecha y hora de la ultima modificacion de la categoria

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre'] #ordena las categorias alfabeticamente

    def __str__(self):
        return self.nombre
