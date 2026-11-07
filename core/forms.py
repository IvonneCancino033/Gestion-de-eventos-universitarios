from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        # No incluimos 'estado' (es automático) ni 'organizador' (lo sacaremos de la sesión)
        fields = ['nombre', 'categoria', 'descripcion', 'fecha_inicio', 'fecha_fin', 'lugar', 'cupo_maximo']
        
        # Widgets para que Bootstrap muestre un calendario con reloj
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'lugar': forms.Select(attrs={'class': 'form-select'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
        }