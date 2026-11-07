from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Evento
from .forms import EventoForm

# Listar y buscar eventos (HU-12)
def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha_inicio')
    return render(request, 'core/evento_list.html', {'eventos': eventos})

# Crear evento (HU-07)
@login_required # Protegemos la vista para que solo usuarios logueados creen eventos
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False) # Pausa el guardado en BD
            evento.organizador = request.user # Asigna al creador
            evento.save() # Ahora sí guarda en SQLite
            return redirect('lista_eventos')
    else:
        form = EventoForm()
        
    return render(request, 'core/evento_form.html', {'form': form})