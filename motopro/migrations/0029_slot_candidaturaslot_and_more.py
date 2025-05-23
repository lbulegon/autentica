# Generated by Django 5.1 on 2025-04-25 06:44

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0028_estabelecimento_cnpj'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('quantidade_motoboys', models.PositiveIntegerField()),
                ('tipo_slot', models.CharField(choices=[('previsto', 'Previsto'), ('extra', 'Extra'), ('urgente', 'Urgente')], default='previsto', max_length=10)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('preenchido', 'Preenchido'), ('cancelado', 'Cancelado')], default='ativo', max_length=12)),
                ('criado_em', models.DateTimeField(default=django.utils.timezone.now)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='motopro.estabelecimento')),
            ],
        ),
        migrations.CreateModel(
            name='CandidaturaSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('recusado', 'Recusado'), ('cancelado', 'Cancelado')], default='pendente', max_length=10)),
                ('data_candidatura', models.DateTimeField(default=django.utils.timezone.now)),
                ('motoboy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidaturas_slot', to='motopro.motoboy')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidaturas', to='motopro.slot')),
            ],
        ),
        migrations.AddConstraint(
            model_name='slot',
            constraint=models.CheckConstraint(condition=models.Q(('quantidade_motoboys__gt', 0)), name='quantidade_motoboys_positiva'),
        ),
        migrations.AlterUniqueTogether(
            name='candidaturaslot',
            unique_together={('slot', 'motoboy')},
        ),
    ]
