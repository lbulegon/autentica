# Generated by Django 5.1 on 2025-04-30 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0042_remove_estabelecimento_contrato_turno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estabelecimento_contrato',
            name='quantidade_vagas',
        ),
    ]
