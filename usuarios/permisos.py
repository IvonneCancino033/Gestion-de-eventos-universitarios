from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


# deja entrar solo a usuarios de esos grupos (o superusuario), si no da error 403
# se usa asi: @grupo_requerido("Organizador") o @grupo_requerido("Administrador", "Organizador")
def grupo_requerido(*grupos):
    def revisar(usuario):
        if usuario.is_superuser or usuario.groups.filter(name__in=grupos).exists():
            return True
        raise PermissionDenied
    return user_passes_test(revisar)
