from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Inscripcion, Asistencia


@receiver(post_save, sender=Inscripcion)
def crear_asistencia(sender, instance, created, **kwargs):

    if created:
        Asistencia.objects.create(
            inscripcion=instance,
            estado=False
        )