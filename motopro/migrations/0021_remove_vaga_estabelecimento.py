# Generated by Django 5.1 on 2025-04-22 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0020_alter_vaga_data_da_vaga'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaga',
            name='estabelecimento',
        ),
    ]
