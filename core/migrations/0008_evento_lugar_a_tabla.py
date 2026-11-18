from django.db import migrations, models
import django.db.models.deletion

# codigo viejo guardado en cada evento -> nombre del lugar en la tabla nueva
CODIGOS = {
    'AUDITORIO_PRINCIPAL': 'Auditorio Principal',
    'AULA_MAGNA': 'Aula Magna',
    'CANCHA_1': 'Cancha 1',
    'GIMNASIO': 'Gimnasio',
    'LAB_BIOINFORMATICA': 'Laboratorio de Bioinformática',
    'SALA_CONFERENCIAS': 'Sala de Conferencias',
}


def copiar_lugares(apps, schema_editor):
    Evento = apps.get_model('core', 'Evento')
    Lugar = apps.get_model('core', 'Lugar')
    for evento in Evento.objects.all():
        nombre = CODIGOS.get(evento.lugar, evento.lugar)  # si el codigo no esta en la lista, usa el texto tal cual
        lugar, _ = Lugar.objects.get_or_create(nombre=nombre)
        evento.lugar_nuevo = lugar
        evento.save(update_fields=['lugar_nuevo'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_precargar_lugares'),
    ]

    operations = [
        # 1. columna nueva (temporal) que apunta a la tabla Lugar, vacia al principio
        migrations.AddField(
            model_name='evento',
            name='lugar_nuevo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventos', to='core.lugar'),
        ),
        # 2. a cada evento se le copia su lugar: texto viejo -> fila de la tabla
        migrations.RunPython(copiar_lugares, migrations.RunPython.noop),
        # 3. se borra la columna vieja de texto (sus datos ya se copiaron)
        migrations.RemoveField(
            model_name='evento',
            name='lugar',
        ),
        # 4. la columna nueva pasa a llamarse "lugar"
        migrations.RenameField(
            model_name='evento',
            old_name='lugar_nuevo',
            new_name='lugar',
        ),
        # 5. ahora que todos los eventos tienen lugar, se vuelve obligatorio
        migrations.AlterField(
            model_name='evento',
            name='lugar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='eventos', to='core.lugar'),
        ),
    ]
