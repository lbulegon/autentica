# Generated by Django 4.2.17 on 2024-12-09 23:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import motopro.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliado_tipo', models.CharField(choices=[('motoboy', 'Motoboy'), ('empresa', 'Empresa'), ('supervisor', 'Supervisor'), ('superuser', 'Super usuario')], max_length=10)),
                ('avaliado_id', models.IntegerField()),
                ('nota', models.PositiveSmallIntegerField(validators=[motopro.models.validate_nota])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='bairro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('descricao', models.TextField(help_text='Descrição da categoria')),
            ],
        ),
        migrations.CreateModel(
            name='cidade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('codigo_ibge', models.CharField(blank=True, max_length=10, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='empresa',
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
                ('bairro_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.bairro')),
                ('cidade_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.cidade')),
            ],
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_total', models.DecimalField(decimal_places=2, help_text='Valor total do empréstimo', max_digits=10)),
                ('numero_parcelas', models.PositiveIntegerField(help_text='Número de parcelas')),
                ('juros_mensal', models.DecimalField(decimal_places=2, help_text='Taxa de juros mensal em %', max_digits=5)),
                ('data_inicio', models.DateField(help_text='Data de início do empréstimo')),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('quitado', 'Quitado'), ('inadimplente', 'Inadimplente')], default='ativo', max_length=15)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='estado',
            fields=[
                ('estado_id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('sigla', models.CharField(max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='motoboy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('cnh', models.CharField(max_length=11, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('placa_moto', models.CharField(max_length=10, unique=True)),
                ('modelo_moto', models.CharField(max_length=100)),
                ('ano_moto', models.IntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2025)])),
                ('cep', models.CharField(max_length=10)),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo'), ('indisponível', 'Indisponível')], default='ativo', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bairro_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.bairro')),
                ('cidade_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.cidade')),
                ('estado_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.estado')),
            ],
        ),
        migrations.CreateModel(
            name='vaga',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('observacoes', models.CharField(max_length=300)),
                ('data_da_vaga', models.DateTimeField(blank=True, null=True)),
                ('valor', models.FloatField()),
                ('status', models.CharField(choices=[('A', 'Aberto'), ('N', 'Em Negociação'), ('P', 'Preenchida')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('empresa_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pedidos', to='motopro.empresa')),
                ('motoboy_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vaga', to='motopro.motoboy')),
            ],
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
                ('bairro_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.bairro')),
                ('cidade_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.cidade')),
                ('estado_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.estado')),
            ],
        ),
        migrations.CreateModel(
            name='ParcelaEmprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_parcela', models.PositiveIntegerField(help_text='Número da parcela')),
                ('valor_parcela', models.DecimalField(decimal_places=2, help_text='Valor da parcela', max_digits=10)),
                ('data_vencimento', models.DateField(help_text='Data de vencimento da parcela')),
                ('data_pagamento', models.DateField(blank=True, help_text='Data em que a parcela foi paga', null=True)),
                ('status', models.CharField(choices=[('pago', 'Pago'), ('pendente', 'Pendente')], default='pendente', max_length=10)),
                ('emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parcelas', to='motopro.emprestimo')),
            ],
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='motoboy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emprestimos', to='motopro.motoboy'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='estado_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='motopro.estado'),
        ),
        migrations.CreateModel(
            name='contratomotoboy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_inicio', models.DateField()),
                ('data_termino', models.DateField()),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('encerrado', 'Encerrado'), ('pendente', 'Pendente')], default='pendente', max_length=10)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('motoboy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contratos_motoboy', to='motopro.motoboy')),
            ],
            options={
                'verbose_name_plural': 'Contratos de Motoboy',
            },
        ),
        migrations.CreateModel(
            name='contratoempresa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_inicio', models.DateField()),
                ('data_termino', models.DateField()),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('encerrado', 'Encerrado'), ('pendente', 'Pendente')], default='pendente', max_length=10)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contratos_empresa', to='motopro.empresa')),
            ],
            options={
                'verbose_name_plural': 'Contratos de Empresa',
            },
        ),
        migrations.AddField(
            model_name='cidade',
            name='todos_estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motopro.estado'),
        ),
        migrations.CreateModel(
            name='categoriamotoboy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontualidade_minima', models.DecimalField(decimal_places=2, help_text='Percentual mínimo de pontualidade, ex: 70%', max_digits=5)),
                ('taxa_aceitacao_minima', models.DecimalField(decimal_places=2, help_text='Taxa mínima de aceitação, ex: 60%', max_digits=5)),
                ('taxa_cancelamento_maxima', models.DecimalField(decimal_places=2, help_text='Taxa máxima de cancelamento, ex: 10%', max_digits=5)),
                ('frequencia_uso_minima', models.IntegerField(help_text='Dias mínimos de uso nos últimos 30 dias')),
                ('entregas_concluidas_minima', models.IntegerField(help_text='Número mínimo de entregas concluídas')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterios', to='motopro.categoria')),
                ('motoboy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='motopro.motoboy')),
            ],
        ),
        migrations.AddField(
            model_name='bairro',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motopro.cidade'),
        ),
        migrations.CreateModel(
            name='avaliacaosupervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.PositiveSmallIntegerField(validators=[motopro.models.validate_nota])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='motopro.supervisor')),
            ],
        ),
        migrations.CreateModel(
            name='avaliacaomotoboy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.PositiveSmallIntegerField(validators=[motopro.models.validate_nota])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
                ('motoboy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='motopro.motoboy')),
            ],
        ),
        migrations.CreateModel(
            name='avaliacaoempresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.PositiveSmallIntegerField(validators=[motopro.models.validate_nota])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='motopro.empresa')),
            ],
        ),
    ]