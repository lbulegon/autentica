# Generated by Django 5.1 on 2025-05-05 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0047_alter_motoboy_alocacao_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaga',
            old_name='horario_fim_padrao',
            new_name='hora_fim_padrao',
        ),
        migrations.RenameField(
            model_name='vaga',
            old_name='horario_inicio_padrao',
            new_name='hora_inicio_padrao',
        ),
    ]
