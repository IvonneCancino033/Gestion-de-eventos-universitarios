from django.db import models #django para crear la base de datos categoria

#Categoria de eventos universitarios
class Categoria(models.Model): #clase categoria
    nombre = models.CharField(max_length=100, unique=True) #nombre de la categoria
    descripcion = models.TextField(blank=True, null=True) #descripcion del evento (opcional)
    estado = models.BooleanField(default=True)
    
    creado_en = models.DateTimeField(auto_now_add=True) #guarda la fecha y hora en que se genera la categoria
    actualizado_en = models.DateTimeField(auto_now=True) #modifica la fecha y hora cuando se edita la categoria

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre'] #ordena las categorias alfabeticamente

    def __str__(self):
        return self.nombre
