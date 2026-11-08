from django import forms
from ...models import Asistencia

class AsistenciaForm(forms.ModelForm):


    ESTADOS = [
        (True, 'Presente'),
        (False, 'Ausente')
    ]

    class Meta:
        model = Asistencia
        fields = ['Id', 'Estado']

        widgets = {
            'Estado': forms.RadioSelect(choices=[(True,'Presente'),(False, 'Ausente')])

        },
        