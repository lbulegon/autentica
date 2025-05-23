# Generated by Django 5.1 on 2025-05-05 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0053_estabelecimento_contrato_valor_tele_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='estabelecimento_fatura',
            name='valor_tele_extra',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estabelecimento_fatura',
            name='valor_vaga_extra',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estabelecimento_fatura',
            name='valor_vaga_fixa',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estabelecimento_fatura',
            name='valor_vaga_spot',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
