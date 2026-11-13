from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UsuarioCrearForm, UsuarioEditarForm
from .permisos import grupo_requerido


@login_required
@grupo_requerido("Administrador")  # solo administradores
def lista_usuarios(request):
    usuarios = User.objects.order_by("username")
    return render(request, "usuarios/usuario_list.html", {"usuarios": usuarios})


@login_required
@grupo_requerido("Administrador")
def crear_usuario(request):
    if request.method == "POST":
        formulario = UsuarioCrearForm(request.POST)
        if formulario.is_valid():
            formulario.save()  # guarda la contraseña con hash
            messages.success(request, "Usuario creado correctamente.")
            return redirect("usuarios:lista")
    else:
        formulario = UsuarioCrearForm()
    return render(request, "usuarios/usuario_form.html",
                  {"formulario": formulario, "titulo": "Nuevo usuario"})


@login_required
@grupo_requerido("Administrador")
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        # instance=usuario para modificar el que ya existe
        formulario = UsuarioEditarForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario modificado correctamente.")
            return redirect("usuarios:lista")
    else:
        formulario = UsuarioEditarForm(instance=usuario)
    return render(request, "usuarios/usuario_form.html",
                  {"formulario": formulario, "titulo": "Editar usuario"})


@login_required
@grupo_requerido("Administrador")
def cambiar_estado_usuario(request, pk):
    # activa o desactiva, no se borra para no perder sus datos
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if usuario == request.user:
            messages.error(request, "No puedes desactivar tu propia cuenta.")
        else:
            usuario.is_active = not usuario.is_active
            usuario.save()
            estado = "activada" if usuario.is_active else "desactivada"
            messages.success(request, f"La cuenta de {usuario.username} fue {estado}.")
    return redirect("usuarios:lista")
