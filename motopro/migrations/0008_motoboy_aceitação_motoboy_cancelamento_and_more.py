# Generated by Django 5.1 on 2025-03-31 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motopro', '0007_comissaomotopro_rankingmotoboy'),
    ]

    operations = [
        migrations.AddField(
            model_name='motoboy',
            name='aceitação',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='motoboy',
            name='cancelamento',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='motoboy',
            name='ranking',
            field=models.CharField(choices=[('Novato', 'Novato'), ('Aspirante', 'Aspirante'), ('Bronze I', 'Bronze I'), ('Bronze II', 'Bronze II'), ('Prata I', 'Prata I'), ('Prata II', 'Prata II'), ('Ouro I', 'Ouro I'), ('Ouro II', 'Ouro II'), ('Platina I', 'Platina I'), ('Platina II', 'Platina II'), ('Diamante I', 'Diamante I'), ('Diamante II', 'Diamante II')], default='Novato', max_length=20),
        ),
        migrations.AddField(
            model_name='motoboy',
            name='supervisor_aprovado',
            field=models.BooleanField(default=False),
        ),
    ]
