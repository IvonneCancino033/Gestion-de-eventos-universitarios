from django.urls import path
from . import views

urlpatterns = [
    #inicio
    path('', views.inicio, name='inicio'),
    
    # categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    
    # eventos 
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/buscar/', views.buscar_eventos, name='buscar_eventos'),
    path('eventos/nuevo/', views.crear_evento, name='crear_evento'),
    path('eventos/editar/<int:pk>/', views.editar_evento, name='editar_evento'),
    path('eventos/cancelar/<int:pk>/', views.cancelar_evento, name='cancelar_evento'),
    path('eventos/eliminar/<int:pk>/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos/inscribirse/<int:pk>/', views.inscribirse_en_evento, name='inscribirse_en_evento'),
    path('eventos/reagendar/<int:pk>/', views.reagendar_evento, name='reagendar_evento'),
    path('eventos/inscripciones/', views.consultar_inscripciones, name='consultar_inscripciones'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),

    # lugares
    path('lugares/', views.lista_lugares, name='lista_lugares'),
    path('lugares/nuevo/', views.crear_lugar, name='crear_lugar'),
    path('lugares/editar/<int:pk>/', views.editar_lugar, name='editar_lugar'),
    path('lugares/estado/<int:pk>/', views.cambiar_estado_lugar, name='cambiar_estado_lugar'),

]
