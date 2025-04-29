
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import re
from django.utils import timezone

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
    placa_regex = r'^[A-Z]{3}-[A-Z0-9]{4}$'  # Regex para verificar formato de placa (ex: ABC-1234 ou ABC-1A2B)
    if not re.match(placa_regex, value):
        raise ValidationError("Placa da moto deve seguir o formato ABC-1234 ou ABC-1A2B.")

def validate_nota(value):
    if value < 0 or value > 9:
        raise ValidationError('A nota deve estar entre 0 e 9.')

class Estado(models.Model):
    id     = models.AutoField(primary_key=True)
    nome   = models.CharField(max_length=100)
    sigla  = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome
class Cidade(models.Model):
    id           = models.IntegerField(primary_key=True)  # Sem `primary_key=True`
    nome         = models.CharField(max_length=255)
    estado       = models.ForeignKey(Estado, on_delete=models.CASCADE)
    codigo_ibge  = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome
class Bairro(models.Model):
    id     = models.AutoField(primary_key=True)  # Ou IntegerField, se você quiser controlar os valores manualmente
    nome   = models.CharField(max_length=255)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class Supervisor(models.Model):
    id                 = models.AutoField(primary_key=True)
    nome               = models.CharField(max_length=255, null=False, blank=False)
    cep                = models.CharField(max_length=10)
    estado             = models.ForeignKey(Estado, on_delete=models.PROTECT)
    cidade             = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    bairro             = models.ForeignKey(Bairro, on_delete=models.PROTECT)
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

class Motoboy(models.Model):
    id                = models.AutoField(primary_key=True)
    nome              = models.CharField(max_length=255, null=False, blank=False)
    apelido           = models.CharField(max_length=255, null=True, blank=True)
    cpf               = models.CharField(max_length=11, unique=False, validators=[validate_cpf])  # CNH do motoboy
    cnh               = models.CharField(max_length=11, unique=False, validators=[validate_cnh])  # CNH do motoboy
    categoria         = models.CharField(max_length=3, null=True, blank=True)
    telefone          = models.CharField(max_length=15, blank=True)  # Telefone de contato
    telefone1         = models.CharField(max_length=15, blank=True)  # Telefone de contato
    email             = models.EmailField(max_length=255, blank=True)  # Email do motoboy
    placa_moto        = models.CharField(max_length=10, unique=False, validators=[validate_placa])  # Placa da moto
    modelo_moto       = models.CharField(max_length=100)  # Modelo da moto
    ano_moto          = models.IntegerField(
        validators=[
            MinValueValidator(2000),  # Ano mínimo para a moto
            MaxValueValidator(datetime.datetime.now().year + 1)  # Ano máximo é o atual +1 para modelo novo
        ]
    )  # Ano de fabricação da moto
    
    cep         = models.CharField(max_length=10)
    estado      = models.ForeignKey(Estado, on_delete=models.PROTECT)
    cidade      = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    bairro      = models.ForeignKey(Bairro, on_delete=models.PROTECT)
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
        ('Bronze III', 'Bronze III'),
        ('Prata I', 'Prata I'),
        ('Prata II', 'Prata II'),
        ('Prata III', 'Prata III'),
        ('Ouro I', 'Ouro I'),
        ('Ouro II', 'Ouro II'),
        ('Ouro III', 'Ouro III'),
        ('Platina I', 'Platina I'),
        ('Platina II', 'Platina II'),
        ('Platina III', 'Platina III'),
        ('Diamante I', 'Diamante I'),
        ('Diamante II', 'Diamante II'),
        ('Diamante III', 'Diamante III'),
    ], default='Novato')
    
    aceitacao        = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Aceitação em %
    cancelamento     = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Cancelamento em %
    
    # Supervisor deve aprovar a mudança de nível
    supervisor_aprovado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
class Estabelecimento(models.Model):
    id                 = models.AutoField(primary_key=True)
    nome               = models.CharField(max_length=255, null=False, blank=False)
    cnpj               = models.CharField(max_length=18)
    cep                = models.CharField(max_length=10)
    estado             = models.ForeignKey(Estado, on_delete=models.PROTECT)
    cidade             = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    bairro             = models.ForeignKey(Bairro, on_delete=models.PROTECT)
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

class EstabelecimentoContrato(models.Model):
    TURNO_CHOICES = [
        ('dia', 'Turno do Dia'),
        ('noite', 'Turno da Noite'),
        ('madrugada', 'Turno da Madrugada'),
    ]   
    estabelecimento    = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    turno              = models.CharField(max_length=10, choices=TURNO_CHOICES)
    valor_atribuido    = models.FloatField(blank=False, null=False)
    horario_inicio     = models.TimeField()
    horario_fim        = models.TimeField()
    quantidade_vagas   = models.PositiveIntegerField()
    data_inicio        = models.DateField(null=True, blank=True)
    data_fim           = models.DateField(null=True, blank=True)
    status             = models.CharField(
        max_length=20,
        choices=[("vigente", "Vigente"), ("vencido", "Vencido"), ("encerrada", "Encerrada"), ("blqueado", "Bloqueado")],
        default="vigente"
    )
    def __str__(self):
       return f'{self.estabelecimento.nome} - {self.get_turno_display()}'

class EstabelecimentoFatura(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    data_referencia = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_alocacoes = models.PositiveIntegerField(default=0)  
    status = models.CharField(
        max_length=20,
        choices=[("aberta", "Aberta"), ("paga", "Paga"), ("vencida", "Vencida")],
        default="aberta"
    )
    gerada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Fatura - ({self.estabelecimento.nome}) {self.data_referencia.strftime("%m/%Y")}'

class Vaga(models.Model):
    id                 = models.AutoField(primary_key=True)
    contrato           = models.ForeignKey(EstabelecimentoContrato, on_delete=models.CASCADE, null=True, blank=True)
    observacao         = models.CharField(max_length=300, null=True, blank=True)
    data_da_vaga       = models.DateField(null=True, blank=True)
    status             = models.CharField(
        max_length=20,
        choices=[("aberta", "Aberta"), ("preenchida", "Preenchida"), ("encerrada", "Encerrada"), ("recusada", "Recusada")],
        default="aberta"
    )
    
    def __str__(self):
        return (
        f"Vaga {self.id} - "
        f"{self.contrato.estabelecimento.nome if self.contrato and self.contrato.estabelecimento else 'Sem estabelecimento'} | "
        f"Turno: {self.contrato.turno if self.contrato and self.contrato.turno else 'Sem turno'} | "
        f"Data: {self.data_da_vaga.strftime('%d/%m/%Y') if self.data_da_vaga else 'Sem data'} | "
        f"Status: {self.get_status_display()}"
    )

class SupervisorMotoboy(models.Model):
    supervisor  = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    motoboy     = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('supervisor', 'motoboy')
    
    def __str__(self):
        return f"Supervisor {self.supervisor.nome} - Motoboy {self.motoboy.nome}"

class SupervisorEstabelecimento(models.Model):
    supervisor      = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('supervisor', 'estabelecimento')
    
    def __str__(self):
        return f"Supervisor {self.supervisor.nome} - Estabelecimento {self.estabelecimento.nome}"

class AlocacaoMotoboy(models.Model):
    vaga                = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    turno               = models.ForeignKey(EstabelecimentoContrato, on_delete=models.CASCADE)  # onde o turno está definido
    motoboy             = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    entregas_realizadas = models.PositiveIntegerField(default=0)
    status              = models.CharField(
        max_length=20,
        choices=[('livre', 'Livre'), ('alocado', 'Alocado')],
        default='livre'
    )
    class Meta:
        unique_together = ('motoboy', 'vaga', 'turno')

    def __str__(self):
        return f"{self.motoboy.nome} - {self.turno} - {self.status}"

class CandidaturaMotoboy(models.Model):
    motoboy     = models.ForeignKey(Motoboy, on_delete=models.CASCADE, related_name="candidaturas")
    vaga        = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name="candidaturas")
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

"""  Esta tabela armazena o ranking e os bônus de cada motoboy conforme o seu desempenho."""
class RankingMotoboy(models.Model):
    motoboy           = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    nivel             = models.CharField(max_length=100, choices=[('Novato', 'Novato'), ('Aspirante', 'Aspirante'), 
                                                      ('Bronze I', 'Bronze I'), ('Bronze II', 'Bronze II'),
                                                      ('Prata I', 'Prata I'), ('Prata II', 'Prata II'),
                                                      ('Ouro I', 'Ouro I'), ('Ouro II', 'Ouro II'),
                                                      ('Platina I', 'Platina I'), ('Platina II', 'Platina II'),
                                                      ('Diamante I', 'Diamante I'), ('Diamante II', 'Diamante II')],
                                                      default='Novato')
    aceitacao         = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cancelamento      = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_por_entrega = models.DecimalField(max_digits=5, decimal_places=2, default=6.00)  # Inicia com R$6,00 por entrega
    
    def __str__(self):
        return f"{self.motoboy.nome} - {self.nivel}"

"""Essa tabela armazena a comissão da MotoPro por cada vaga."""
class ComissaoMotopro(models.Model):
    vaga           = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    comissao       = models.DecimalField(max_digits=8, decimal_places=2)  # Exemplo: 15% da vaga
    data_pagamento = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comissão Vaga {self.vaga.id} - R${self.comissao}"

class Configuracao(models.Model):
    turno_padrao = models.CharField(max_length=10, choices=[
        ('dia', 'Turno do Dia'),
        ('noite', 'Turno da Noite'),
    ], default='dia')

    horario_inicio_padrao = models.TimeField(default='08:00')
    horario_fim_padrao    = models.TimeField(default='18:00')
    valor_padrao_por_vaga = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    sistema_ativo         = models.BooleanField(default=True)
    ultima_atualizacao    = models.DateTimeField(auto_now=True)
    versao                = models.CharField(max_length=20, default='1.0.0')

    def __str__(self):
        return "Configurações do Sistema"

class Slot(models.Model):
    TIPO_SLOT_CHOICES = [
        ('previsto', 'Previsto'),
        ('extra', 'Extra'),
        ('urgente', 'Urgente'),
    ]

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('preenchido', 'Preenchido'),
        ('cancelado', 'Cancelado'),
    ]

    estabelecimento     = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, related_name='slots')
    data                = models.DateField()
    hora_inicio         = models.TimeField()
    hora_fim            = models.TimeField()
    quantidade_motoboys = models.PositiveIntegerField()
    tipo_slot           = models.CharField(max_length=10, choices=TIPO_SLOT_CHOICES, default='previsto')
    status              = models.CharField(max_length=12, choices=STATUS_CHOICES, default='ativo')
    criado_em           = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade_motoboys__gt=0), name='quantidade_motoboys_positiva')
        ]

    def __str__(self):
        return f"{self.estabelecimento.nome} | {self.data} | {self.hora_inicio}-{self.hora_fim}"

class CandidaturaSlot(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
    ]

    slot             = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='candidaturas')
    motoboy          = models.ForeignKey(Motoboy, on_delete=models.CASCADE, related_name='candidaturas_slot')
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_candidatura = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('slot', 'motoboy')

    def __str__(self):
        return f"{self.motoboy.nome} → {self.slot}"

class VagaSlot(models.Model):
    contrato    = models.ForeignKey(EstabelecimentoContrato, on_delete=models.CASCADE)
    data        = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim    = models.TimeField()
    motoboy     = models.ForeignKey(Motoboy, null=True, blank=True, on_delete=models.SET_NULL)
    status      = models.CharField(
        max_length=20,
        choices=[("disponivel", "Disponível"), ("ocupada", "Ocupada"), ("cancelada", "Cancelada")],
        default="disponivel"
    )

    class Meta:
        unique_together = ('contrato', 'data', 'hora_inicio')

    def __str__(self):
        return f'{self.contrato.estabelecimento.nome} | {self.data} | {self.hora_inicio} - {self.hora_fim}'
