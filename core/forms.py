from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models.evento import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'nombre', 
            'categoria', 
            'descripcion', 
            'fecha_inicio', 
            'fecha_fin', 
            'lugar', 
            'cupo_maximo'
        ]
        
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lugar': forms.Select(attrs={'class': 'form-select'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        lugar = cleaned_data.get('lugar')
        current_year = timezone.now().year

        if fecha_inicio and fecha_fin:
            # Validar que no se programen eventos en años pasados
            if fecha_inicio.year < current_year:
                raise ValidationError({
                    'fecha_inicio': "No se pueden programar eventos en años que ya pasaron."
                })
            # Validar que la fecha de fin sea posterior a la de inicio
            if fecha_fin.year > current_year:
                raise ValidationError({
                    'fecha_fin': "No se pueden programar eventos en años que ya pasaron"
                })

            if fecha_inicio >= fecha_fin:
                raise ValidationError({
                    'fecha_fin': "La fecha y hora de fin debe ser posterior a la de inicio."
                })

            # Validar cruces de horarios en el mismo lugar físico
            if lugar:
                conflictos = Evento.objects.filter(
                    lugar=lugar,
                    fecha_inicio__lt=fecha_fin,
                    fecha_fin__gt=fecha_inicio
                ).exclude(estado='CANCELADO') # Ignoramos los cancelados

                # Si estamos editando el evento, nos excluimos a nosotros mismos de la busqueda
                if self.instance and self.instance.pk:
                    conflictos = conflictos.exclude(pk=self.instance.pk)

                if conflictos.exists():
                    raise ValidationError(
                        "Ya existe otro evento activo programado en este mismo recinto (lugar) y con el mismo horario seleccionado."
                    )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M']