
from django.urls import path
from .views.pagina_principal_asistencia import principal_staff
from .views.asistencia_views import buscar_participante
from .views.registrar_asistencia import registrar_asistencia
from .views.mostrar_asistencia import mostrar
from .views.estadisticas import estadisticas
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        'buscar_participante/',
        buscar_participante,
        name='buscar_participante'
    ),

    path(
        'registrar_asistencia/<int:inscripcion_id>/',
        registrar_asistencia,
        name='registrar_asistencia'
    ),
    
    path(
        'mostrar_asistencia/<int:evento_id>/',
        mostrar,
        name='mostrar_asistencia'
    ),
    
    path(
        'asistencia/',
        principal_staff,
        name='pagina_principal_asistencia'
    ),

    path(
        'estadisticas/<int:evento_id>/',
        estadisticas,
        name='estadisticas'
    ),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]