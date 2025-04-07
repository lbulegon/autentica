
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import re

# Função de validação para CPF
def validate_cpf(value):
    cpf_regex = r'^\d{11}$'  # Regex para verificar se o CPF possui 11 dígitos
    if not re.match(cpf_regex, value):
        raise ValidationError("CPF deve ter 11 dígitos numéricos.")

# Função de validação para CNH
def validate_cnh(value):
    cnh_regex = r'^\d{11}$'  # Regex para verificar se a CNH possui 11 dígitos
    if not re.match(cnh_regex, value):
        raise ValidationError("CNH deve ter 11 dígitos numéricos.")

# Função de validação para placa de moto
def validate_placa(value):
    placa_regex = r'^[A-Z]{3}-\d{4}$'  # Regex para verificar formato de placa (ex: ABC-1234)
    if not re.match(placa_regex, value):
        raise ValidationError("Placa da moto deve seguir o formato ABC-1234.")

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
    id     = models.AutoField(primary_key=True)  # Ou IntegerField, se você quiser controlar os valores manualmente
    nome   = models.CharField(max_length=255)
    cidade = models.ForeignKey('cidade', on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class supervisor(models.Model):
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
    finished_at        = models.DateTimeField(null=True) 
    status             = models.CharField(max_length=20, choices=[
                        ('ativo', 'Ativo'),
                        ('inativo', 'Inativo'),
                        ], default='ativo')  # Status do motoboy
    def __str__(self):
        return self.nome

class motoboy(models.Model):
    id           = models.AutoField(primary_key=True)
    nome         = models.CharField(max_length=255, null=False, blank=False)
    cpf          = models.CharField(max_length=11, unique=True, validators=[validate_cpf])  # CNH do motoboy
    cnh          = models.CharField(max_length=11, unique=True, validators=[validate_cnh])  # CNH do motoboy
    telefone     = models.CharField(max_length=15, blank=True)  # Telefone de contato
    email        = models.EmailField(max_length=255, blank=True)  # Email do motoboy
    placa_moto   = models.CharField(max_length=10, unique=True, validators=[validate_placa])  # Placa da moto
    modelo_moto  = models.CharField(max_length=100)  # Modelo da moto
    ano_moto     = models.IntegerField(
        validators=[
            MinValueValidator(2000),  # Ano mínimo para a moto
            MaxValueValidator(datetime.datetime.now().year + 1)  # Ano máximo é o atual +1 para modelo novo
        ]
    )  # Ano de fabricação da moto
    
    cep         = models.CharField(max_length=10)
    estado      = models.ForeignKey('Estado', on_delete=models.PROTECT)
    cidade      = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    bairro      = models.ForeignKey('Bairro', on_delete=models.PROTECT)
    logradouro  = models.CharField(max_length=255)
    numero      = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    
    # Status do motoboy
    status = models.CharField(max_length=20, choices=[
        ('alocado', 'Alocado'),
        ('livre', 'Livre'),
        ('inativo', 'Inativo'),
        ('em_viagem', 'Em viagem'),
    ], default='livre') 
    
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação do registro
    updated_at = models.DateTimeField(auto_now=True)  # Data da última atualização
       # Atributos adicionais para o sistema de ranking
    ranking          = models.CharField(max_length=20, choices=[
        ('Novato', 'Novato'),
        ('Aspirante', 'Aspirante'),
        ('Bronze I', 'Bronze I'),
        ('Bronze II', 'Bronze II'),
        ('Prata I', 'Prata I'),
        ('Prata II', 'Prata II'),
        ('Ouro I', 'Ouro I'),
        ('Ouro II', 'Ouro II'),
        ('Platina I', 'Platina I'),
        ('Platina II', 'Platina II'),
        ('Diamante I', 'Diamante I'),
        ('Diamante II', 'Diamante II'),
    ], default='Novato')
    
    aceitacao        = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Aceitação em %
    cancelamento     = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Cancelamento em %
    
    # Supervisor deve aprovar a mudança de nível
    supervisor_aprovado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
class estabelecimento(models.Model):
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
    id                 = models.AutoField(primary_key=True)
    estabelecimento    = models.ForeignKey(estabelecimento, on_delete=models.PROTECT, related_name='pedidos')
    motoboy            = models.OneToOneField(motoboy, on_delete=models.SET_NULL, null=True, blank=True, related_name='vaga')
    observacoes        = models.CharField(max_length=300, null=False, blank=False)
    data_da_vaga       = models.DateTimeField(null=True, blank=True)
    valor              = models.FloatField(blank=False, null=False)
    created_at         = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    hora_inicio        = models.TimeField(null=True, blank=True)
    hora_fim           = models.TimeField(null=True, blank=True)
    turno              = models.CharField(
        max_length=20,
        choices=[("manhã", "Manhã"), ("tarde", "Tarde"), ("noite", "Noite")],
        null=True,
        blank=True
    )
    status             = models.CharField(
        max_length=20,
        choices=[("aberta", "Aberta"), ("preenchida", "Preenchida"), ("encerrada", "Encerrada"), ("recusada", "Recusada")],
        default="aberta"
    )

    def save(self, *args, **kwargs):
        if self.motoboy:
            if self.motoboy.status != "alocado":  # Verifica se o motoboy não está alocado
                self.motoboy.status = "alocado"
                self.motoboy.save()
        elif self.pk:  # Se não houver motoboy e a vaga já foi salva
            old_vaga = vaga.objects.get(pk=self.pk)
            if old_vaga.motoboy:  # Verifica se havia um motoboy antes
                old_vaga.motoboy.status = "livre"
                old_vaga.motoboy.save()

        super().save(*args, **kwargs)

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




class supervisormotoboy(models.Model):
    supervisor  = models.ForeignKey(supervisor, on_delete=models.CASCADE)
    motoboy     = models.ForeignKey(motoboy, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('supervisor', 'motoboy')
    
    def __str__(self):
        return f"Supervisor {self.supervisor.nome} - Motoboy {self.motoboy.nome}"

class supervisorestabelecimento(models.Model):
    supervisor      = models.ForeignKey(supervisor, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(estabelecimento, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('supervisor', 'estabelecimento')
    
    def __str__(self):
        return f"Supervisor {self.supervisor.nome} - Estabelecimento {self.estabelecimento.nome}"


"""
Essa tabela vai armazenar as entregas feitas pelos motoboys e permitir calcular o valor pago a cada motoboy.
"""
class entrega(models.Model):
    vaga = models.ForeignKey(vaga, on_delete=models.CASCADE)
    motoboy = models.ForeignKey(motoboy, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2)
    data_entrega = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entrega {self.id} - Motoboy: {self.motoboy.nome} - Vaga {self.vaga.id}"



"""  Esta tabela armazena o ranking e os bônus de cada motoboy conforme o seu desempenho."""
class rankingMotoboy(models.Model):
    motoboy = models.ForeignKey(motoboy, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=100, choices=[('Novato', 'Novato'), ('Aspirante', 'Aspirante'), 
                                                      ('Bronze I', 'Bronze I'), ('Bronze II', 'Bronze II'),
                                                      ('Prata I', 'Prata I'), ('Prata II', 'Prata II'),
                                                      ('Ouro I', 'Ouro I'), ('Ouro II', 'Ouro II'),
                                                      ('Platina I', 'Platina I'), ('Platina II', 'Platina II'),
                                                      ('Diamante I', 'Diamante I'), ('Diamante II', 'Diamante II')],
                                                      default='Novato')
    aceitação = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cancelamento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_por_entrega = models.DecimalField(max_digits=5, decimal_places=2, default=6.00)  # Inicia com R$6,00 por entrega
    
    def __str__(self):
        return f"{self.motoboy.nome} - {self.nivel}"



"""Essa tabela armazena a comissão da MotoPro por cada vaga."""

class comissaomotopro(models.Model):
    vaga = models.ForeignKey(vaga, on_delete=models.CASCADE)
    comissao = models.DecimalField(max_digits=8, decimal_places=2)  # Exemplo: 15% da vaga
    data_pagamento = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comissão Vaga {self.vaga.id} - R${self.comissao}"
