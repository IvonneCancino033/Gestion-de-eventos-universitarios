from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# formulario para crear usuario, UserCreationForm ya pide la contraseña 2 veces
class UsuarioCrearForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Correo")

    

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    # que no se repita el correo
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email


# formulario para editar, sin contraseña
class UsuarioEditarForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Correo")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {"username": "Nombre de usuario"}

    # el correo no puede ser igual al de otro usuario (excluye al mismo)
    def clean_email(self):
        email = self.cleaned_data["email"]
        existe = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("Ya existe otro usuario con este correo.")
        return email


# registro publico, usa los mismos campos y validaciones que crear usuario
class RegistroForm(UsuarioCrearForm):
    pass
