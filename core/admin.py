from django.contrib import admin
from .models.categoria import Categoria
from .models.evento import Evento
from .models.inscripcion import Inscripcion
from .models.asistencia import Asistencia

@admin.register(Categoria) #registrar categoria
class CategoriaAdmin(admin.ModelAdmin):#clase catgeoria en el panel
    list_display = ('nombre', 'estado', 'creado_en') #lo que se mostrara en la tabla
    search_fields = ('nombre',) 


@admin.register(Evento) #registrar evento
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lugar', 'estado', 'fecha_inicio', 'fecha_fin') #lo que se mostrara en la tabla
    search_fields = ('nombre',) #para filtrar los eventos por nombre


admin.site.register(Inscripcion) #registrar la tabla de inscripcion
admin.site.register(Asistencia) #registra la tabla de asistencias
