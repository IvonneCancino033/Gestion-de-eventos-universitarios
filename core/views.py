from django.shortcuts import render, redirect
from .models import Categoria

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