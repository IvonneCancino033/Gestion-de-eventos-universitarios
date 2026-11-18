
#vistas de la pagina web
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models.categoria import Categoria
from .models.evento import Evento
from .forms import EventoForm
from django.db.models import Count, ExpressionWrapper, F, IntegerField, Q
from .forms import BuscarEventoForm, LugarForm
from usuarios.permisos import grupo_requerido
from django.contrib import messages
from django.utils import timezone
from .models.lugar import Lugar
from .models import Inscripcion


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
# HU-12: buscar eventos por nombre, categoría, fecha o estado
@login_required
def buscar_eventos(request):
    form = BuscarEventoForm(request.GET or None)

    # Cupos disponibles = cupo máximo - inscripciones activas
    eventos = (
        Evento.objects.select_related("categoria")
        .annotate(
            inscritos=Count("inscripciones", filter=Q(inscripciones__estado="ACTIVA"))
        )
        .annotate(
            cupos_disponibles=ExpressionWrapper(
                F("cupo_maximo") - F("inscritos"), output_field=IntegerField()
            )
        )
        .order_by("fecha_inicio") 
    )

    if form.is_valid():
        datos = form.cleaned_data
        if datos["nombre"]:
            eventos = eventos.filter(nombre__icontains=datos["nombre"].strip())
        if datos["categoria"]:
            eventos = eventos.filter(categoria=datos["categoria"])
        if datos["fecha"]:
            # Eventos que ocurren ese día (incluye eventos de varios días)
            eventos = eventos.filter(
                fecha_inicio__date__lte=datos["fecha"],
                fecha_fin__date__gte=datos["fecha"],
            )
        if datos["estado"]:
            eventos = eventos.filter(estado=datos["estado"])

    return render(request, "core/evento_buscar.html", {"form": form, "eventos": eventos})

#HU-13: inscribirse en un evento 

@login_required
@grupo_requerido("Participante")
def inscribirse_en_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        ocupados = evento.inscripciones.filter(estado = 'ACTIVA').count()
        disponibles = evento.cupo_maximo - ocupados

    #para poder inscribirse el evento debe estar abierto a inscripciones
        if evento.estado not in ('DISPONIBLE', 'REAGENDADO'):
            messages.error (request, "Este evento ya no acepta más inscripciones.")
    #no se puede inscribir en un evento terminado
        elif evento.fecha_fin <= timezone.now():
            messages.error (request, "Este evento ha finalizado.") 
    #no puede tener dos inscripciones activas en el mismo evento 

        elif evento.inscripciones.filter(usuario=request.user, estado = 'ACTIVA'). exists():
            messages.error (request, "Ya estás inscrito en este evento.")

    #para poder inscribirse debe haber al menos un cupo
        elif disponibles <= 0:
            messages.error(request, "No hay cupos disponibles para este evento.")

        else:
            Inscripcion.objects.create(usuario=request.user, evento=evento)
            messages.success(request, f"Te inscribiste en {evento.nombre}.")

    return redirect ('lista_eventos')

# HU-14: consultar inscripciones de un evento

@login_required
@grupo_requerido("Organizador", "Administrador")
def consultar_inscripciones(request):
    #  solo los eventos de este organizador
    mis_eventos = Evento.objects.filter(organizador=request.user).order_by('-fecha_inicio')

    # Valores por defecto (cuando aún no se elige evento)
    evento = None
    inscripciones = []
    ocupados = 0
    disponibles = 0

    # Si el usuario eligió un evento en el desplegable 
    evento_id = request.GET.get('evento')
    if evento_id:
        evento = get_object_or_404(mis_eventos, pk=evento_id)
        #  participantes y estado de cada inscripción
        inscripciones = evento.inscripciones.select_related('usuario').order_by('fecha_inscripcion')
        #  cupos ocupados y disponibles
        ocupados = inscripciones.filter(estado='ACTIVA').count()
        disponibles = evento.cupo_maximo - ocupados

    return render(request, 'core/inscripciones_evento.html', {
        'mis_eventos': mis_eventos,
        'evento': evento,
        'inscripciones': inscripciones,
        'ocupados': ocupados,
        'disponibles': disponibles,
    })

# --- VISTAS DE LUGARES ---

#  muestra todos los lugares, incluidos los precargados
@login_required
@grupo_requerido("Administrador")
def lista_lugares(request):
    lugares = Lugar.objects.all()
    return render(request, 'core/lugar_list.html', {'lugares': lugares})


# crear
@login_required
@grupo_requerido("Administrador")
def crear_lugar(request):
    if request.method == 'POST':
        form = LugarForm(request.POST)
        if form.is_valid():
            lugar = form.save()
            messages.success(request, f'Lugar "{lugar.nombre}" creado correctamente.')  # criterio 4
            return redirect('lista_lugares')
    else:
        form = LugarForm()
    return render(request, 'core/lugar_form.html', {'form': form, 'titulo': 'Nuevo lugar'})


#  modificar
@login_required
@grupo_requerido("Administrador")
def editar_lugar(request, pk):
    lugar = get_object_or_404(Lugar, pk=pk)
    if request.method == 'POST':
        form = LugarForm(request.POST, instance=lugar)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lugar "{lugar.nombre}" actualizado correctamente.')  # criterio 4
            return redirect('lista_lugares')
    else:
        form = LugarForm(instance=lugar)
    return render(request, 'core/lugar_form.html', {'form': form, 'titulo': 'Modificar lugar'})


# desactivar (o volver a activar)
@login_required
@grupo_requerido("Administrador")
def cambiar_estado_lugar(request, pk):
    lugar = get_object_or_404(Lugar, pk=pk)
    if request.method == 'POST':
        lugar.estado = not lugar.estado
        lugar.save(update_fields=['estado', 'actualizado_en'])
        accion = 'activado' if lugar.estado else 'desactivado'
        messages.success(request, f'Lugar "{lugar.nombre}" {accion}.')  # criterio 4
    return redirect('lista_lugares')
