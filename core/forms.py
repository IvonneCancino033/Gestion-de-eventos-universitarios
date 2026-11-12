from django import forms

from .models import Categoria, Evento


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
