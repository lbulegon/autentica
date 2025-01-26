
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime

def validate_nota(value):
    if value < 0 or value > 9:
        raise ValidationError('A nota deve estar entre 0 e 9.')

class estado(models.Model):
    id     = models.AutoField(primary_key=True)
    nome   = models.CharField(max_length=100)
    sigla  = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome
class cidade(models.Model):
    id           = models.IntegerField(primary_key=True)  # Sem `primary_key=True`
    nome         = models.CharField(max_length=255)
    estado       = models.ForeignKey(estado, on_delete=models.CASCADE)
    codigo_ibge  = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome


class bairro(models.Model):
    id           = models.IntegerField(primary_key=True)  
    nome         = models.CharField(max_length=255)
    cidade       = models.ForeignKey(cidade, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'cidade'], name='pk_bairro_id_cidade'),
        ]
        unique_together = ('id', 'cidade')

    def __str__(self):
        return self.nome


class motoboy(models.Model):
    id                 = models.AutoField(primary_key=True)
    nome               = models.CharField(max_length=255, null=False, blank=False)
    cpf                = models.CharField(max_length=11, unique=True)  # CNH do motoboy
    cnh                = models.CharField(max_length=11, unique=True)  # CNH do motoboy
    telefone           = models.CharField(max_length=15, blank=True)  # Telefone de contato
    email              = models.EmailField(max_length=255, blank=True)  # Email do motoboy
    placa_moto         = models.CharField(max_length=10, unique=True)  # Placa da moto
    modelo_moto        = models.CharField(max_length=100)  # Modelo da moto
    ano_moto           = models.IntegerField(
                            validators=[
                                MinValueValidator(2000),                             # Ano mínimo para a moto
                                MaxValueValidator(datetime.datetime.now().year + 1)  # Ano máximo é o atual +1 para modelo novo
                            ]
                        )  # Ano de fabricação da moto
   
    cep                = models.CharField(max_length=10)
    estado             = models.ForeignKey(estado, on_delete=models.PROTECT)
    cidade             = models.ForeignKey(cidade, on_delete=models.PROTECT)
    bairro             = models.ForeignKey(bairro, on_delete=models.PROTECT)
    logradouro         = models.CharField(max_length=255)
    numero             = models.CharField(max_length=10)
    complemento        = models.CharField(max_length=100, blank=True)
    status             = models.CharField(max_length=20, choices=[
                        ('alocado', 'Alocado'),
                        ('livre', 'Livre'),
                        ('inativo', 'Inativo'),
                        ], default='livre')  # Status do motoboy

    
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data da última atualização
     
    def __str__(self):
        return self.nome

class empresa(models.Model):
    id                 = models.AutoField(primary_key=True)
    nome               = models.CharField(max_length=255, null=False, blank=False)
    cep                = models.CharField(max_length=10)
    estado             = models.ForeignKey(estado, on_delete=models.PROTECT)
    cidade             = models.ForeignKey(cidade, on_delete=models.PROTECT)
    bairro             = models.ForeignKey(bairro, on_delete=models.PROTECT)
    logradouro         = models.CharField(max_length=255)
    numero             = models.CharField(max_length=10)
    complemento        = models.CharField(max_length=100, blank=True)
    created_at         = models.DateTimeField(auto_now_add= True, null=False, blank=False)
    deadline           = models.DateTimeField(null=False, blank=False)
   
    status             = models.CharField(max_length=20, choices=[
                        ('ativo', 'Ativo'),
                        ('inativo', 'Inativo'),
                        ], default='ativo')  # Status do motoboy


    def __str__(self):
        return self.nome
    
class vaga(models.Model):
    id            = models.AutoField(primary_key=True)
    empresa       = models.ForeignKey(empresa, on_delete=models.PROTECT, related_name='pedidos')
    motoboy       = models.OneToOneField(motoboy, on_delete=models.PROTECT, null=True, blank=True, related_name='vaga')  # O campo pode ser NULL e deixado em branco
    observacoes   = models.CharField(max_length=300, null=False, blank=False)
    data_da_vaga  = models.DateTimeField(null=True, blank=True)  # Campo editável
    valor         = models.FloatField(blank=False, null=False)
    created_at    = models.DateTimeField(auto_now_add= True, null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ("aberta", "Aberta"),
            ("preenchida", "Encerrada"),
            ("encerrada", "Encerrada"),
            ("recusada", "Recusada"),
        ],
        default="Aberta"
        )  
    def __str__(self):
        return f"Vaga {self.id} - Status: {self.get_status_display()}"


class candidatura(models.Model):
    motoboy     = models.ForeignKey(motoboy, on_delete=models.CASCADE, related_name="candidaturas")
    vaga        = models.ForeignKey(vaga, on_delete=models.CASCADE, related_name="candidaturas")
    status      = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("aprovada", "Aprovada"),
            ("recusada", "Recusada")
        ],
        default="Pendente"
    )
    data_candidatura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.motoboy.nome} - {self.vaga.titulo} ({self.status})"
