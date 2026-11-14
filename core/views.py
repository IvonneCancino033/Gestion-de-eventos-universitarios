
#vistas de la pagina web
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models.categoria import Categoria
from .models.evento import Evento
from .forms import EventoForm


# --- VISTA PRINCIPAL ---
@login_required
def inicio(request):
    return render(request, "core/index.html")


# --- VISTAS DE CATEGORIAS ---
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('-creado_en')
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado') == 'on'
        
        if nombre and nombre.strip():
            Categoria.objects.create(
                nombre=nombre.strip(),
                descripcion=descripcion.strip() if descripcion else '',
                estado=estado
            )
            return redirect('lista_categorias')
            
    return render(request, 'core/categoria_form.html')

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado') == 'on'
        
        if nombre and nombre.strip():
            categoria.nombre = nombre.strip()
            categoria.descripcion = descripcion.strip() if descripcion else ''
            categoria.estado = estado
            categoria.save()
            return redirect('lista_categorias')
            
    return render(request, 'core/categoria_form.html', {'categoria': categoria})



# --- VISTAS DE EVENTOS ---
@login_required
def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha_inicio')
    return render(request, 'core/evento_list.html', {'eventos': eventos})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user # asigna el usuario en sesion
            evento.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'core/evento_form.html', {'form': form, 'titulo': 'Organizar Nuevo Evento'})

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    # Control de acceso: Solo el organizador o staff pueden modificar (HU-09)
    if request.user != evento.organizador and not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para modificar este evento.")
        
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'core/evento_form.html', {'form': form, 'titulo': 'Modificar Evento'})

@login_required
def cancelar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    # Control de acceso (HU-10)
    if request.user != evento.organizador and not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para cancelar este evento.")
        
    if request.method == 'POST':
        evento.estado = 'CANCELADO'
        evento.save(update_fields=['estado'])
    return redirect('lista_eventos')

@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    # Control de acceso (HU-11)
    if request.user != evento.organizador and not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para eliminar este evento.")
        
    if request.method == 'POST':
        evento.delete()
    return redirect('lista_eventos')

@login_required
def reagendar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    
    # Control de acceso: Solo organizador o staff pueden reagendar
    if request.user != evento.organizador and not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para reagendar este evento.")
        
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento_editado = form.save(commit=False)
            evento_editado.estado = 'REAGENDADO'
            evento_editado.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
        
    return render(request, 'core/evento_form.html', {
        'form': form, 
        'titulo': f'Reagendar Evento: {evento.nombre}'
    })