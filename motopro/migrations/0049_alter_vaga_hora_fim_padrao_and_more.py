# Generated by Django 5.1 on 2025-05-05 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0048_rename_horario_fim_padrao_vaga_hora_fim_padrao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaga',
            name='hora_fim_padrao',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='hora_inicio_padrao',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='status',
            field=models.CharField(choices=[('aberta', 'Aberta'), ('reservada', 'Reservada'), ('ocupada', 'Ocupada'), ('finalizada', 'Finalizada'), ('cancelada', 'Cancelada')], default='disponivel', max_length=20),
        ),
    ]
