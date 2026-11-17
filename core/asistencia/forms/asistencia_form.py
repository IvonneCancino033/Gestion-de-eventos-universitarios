from django import forms
from ...models import Asistencia

class AsistenciaForm(forms.ModelForm):

    class Meta:
        model = Asistencia
        fields = ['estado']

        widgets = {
            'estado': forms.RadioSelect(choices=[
                    (True, 'Presente'),
                    (False, 'Ausente')
                ])

        }


        