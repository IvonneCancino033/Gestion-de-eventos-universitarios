from django import forms
from django.core.exceptions import ValidationError
from .models.evento import Evento
from django.db.models import Q

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

        if fecha_inicio and fecha_fin:
            # 1. Validar que la fecha de fin sea posterior a la de inicio
            if fecha_inicio >= fecha_fin:
                raise ValidationError({
                    'fecha_fin': "La fecha y hora de fin debe ser posterior a la de inicio."
                })

            # 2. Validar cruces de horarios en el mismo lugar físico
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
                        "Ya existe otro evento activo programado en este mismo recinto (lugar) que se cruza con el horario seleccionado."
                    )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M']
        # solo lugares activos (y el actual, si se edita un evento cuyo lugar se desactivo)
        self.fields['lugar'].queryset = Lugar.objects.filter(
            Q(estado=True) | Q(pk=self.instance.lugar_id)
        )
        self.fields['lugar'].empty_label = 'Selecciona un lugar'


from .models import Categoria, Evento, Lugar


class BuscarEventoForm(forms.Form):
  

    nombre = forms.CharField(
        label="Nombre",
        required=False,
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: Torneo de fútbol"}
        ),
    )
    categoria = forms.ModelChoiceField(
        label="Categoría",
        queryset=Categoria.objects.filter(estado=True),
        required=False,
        empty_label="Todas",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    fecha = forms.DateField(
        label="Fecha",
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
        ),
    )
    estado = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[("", "Todos")] + Evento.ESTADOS,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

# HU-06 formulario para crear y modificar lugares
class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ['nombre']
        labels = {'nombre': 'Nombre del lugar'}
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sala 201'}),
        }

    # rechazar un lugar con un nombre ya existente
    def clean_nombre(self):
        nombre = ' '.join(self.cleaned_data['nombre'].split())  # quita espacios de sobra
        repetido = Lugar.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:  # si estamos editando, no compararse consigo mismo
            repetido = repetido.exclude(pk=self.instance.pk)
        if repetido.exists():
            raise forms.ValidationError('Ya existe un lugar con ese nombre.')
        return nombre
