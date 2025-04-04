# Generated by Django 5.1 on 2025-03-28 04:07

import django.db.models.deletion
import motopro.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bairro',
            options={'managed': False},
        ),
        migrations.RenameField(
            model_name='vaga',
            old_name='empresa',
            new_name='estabelecimento',
        ),
        migrations.AlterField(
            model_name='motoboy',
            name='cnh',
            field=models.CharField(max_length=11, unique=True, validators=[motopro.models.validate_cnh]),
        ),
        migrations.AlterField(
            model_name='motoboy',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, validators=[motopro.models.validate_cpf]),
        ),
        migrations.AlterField(
            model_name='motoboy',
            name='placa_moto',
            field=models.CharField(max_length=10, unique=True, validators=[motopro.models.validate_placa]),
        ),
        migrations.AlterField(
            model_name='motoboy',
            name='status',
            field=models.CharField(choices=[('alocado', 'Alocado'), ('livre', 'Livre'), ('inativo', 'Inativo'), ('em_viagem', 'Em viagem')], default='livre', max_length=20),
        ),
        migrations.CreateModel(
            name='supervisor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('cep', models.CharField(max_length=10)),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('finished_at', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=20)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.cidade')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.estado')),
            ],
        ),
        migrations.RenameModel(
            old_name='empresa',
            new_name='estabelecimento',
        ),
        migrations.CreateModel(
            name='supervisorestabelecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motopro.estabelecimento')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motopro.supervisor')),
            ],
            options={
                'unique_together': {('supervisor', 'estabelecimento')},
            },
        ),
        migrations.CreateModel(
            name='supervisormotoboy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('motoboy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motopro.motoboy')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motopro.supervisor')),
            ],
            options={
                'unique_together': {('supervisor', 'motoboy')},
            },
        ),
    ]
