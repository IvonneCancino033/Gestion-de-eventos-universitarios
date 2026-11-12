from django.contrib.auth.decorators import login_required
from django.db.models import Count, ExpressionWrapper, F, IntegerField, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BuscarEventoForm
from .models import Categoria, Evento


@login_required
def inicio(request):
    return render(request, "core/index.html")


# Listar categorías
def lista_categorias(request): #funcion vista
    categorias = Categoria.objects.all() #consulta para traer los datos de la base de datos
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

# Crear categoría
def crear_categoria(request): #procesa el formulario
    if request.method == 'POST': #verififca que se hayan enviado los datos
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        #se extraen los datos de los campos nombre y descripcion
        
        # Validar en el servidor que el nombre no venga vacío
        if nombre and nombre.strip():
            Categoria.objects.create(
                nombre=nombre.strip(),
                descripcion=descripcion.strip() if descripcion else ''
            )
            return redirect('lista_categorias')
            
    return render(request, 'core/categoria_form.html')

# 3. Editar categoría
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        
        if nombre and nombre.strip():
            categoria.nombre = nombre.strip()
            categoria.descripcion = descripcion.strip() if descripcion else ''
            categoria.save()
            return redirect('lista_categorias')
            
    return render(request, 'core/categoria_form.html', {'categoria': categoria})


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
        .order_by("fecha_inicio")  # Count() anula el ordering del Meta
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

    return render(request, "core/evento_list.html", {"form": form, "eventos": eventos})
