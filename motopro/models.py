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

class Estado(models.Model):
    id     = models.AutoField(primary_key=True)
    nome   = models.CharField(max_length=100)
    sigla  = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome
class Cidade(models.Model):
    id           = models.AutoField(primary_key=True)
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

class Motoboy_Nivel(models.Model):
    nome      = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True)
    ordem     = models.PositiveIntegerField(unique=True)  # Para ordenação dos rankings

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['ordem']


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
    
    created_at   = models.DateTimeField(auto_now_add=True)  # Data de criação do registro
    updated_at   = models.DateTimeField(auto_now=True)  # Data da última atualização
    nivel        = models.ForeignKey(Motoboy_Nivel, on_delete=models.PROTECT)
    aceitacao    = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Aceitação em %
    cancelamento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Cancelamento em %
    
    # Supervisor deve aprovar a mudança de nível
    supervisor_aprovado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
class Motoboy_Contrato(models.Model):
    motoboy               = models.ForeignKey(Motoboy, on_delete=models.CASCADE, related_name='contracts')
    data_inicio           = models.DateField()
    data_fim              = models.DateField(null=True, blank=True)  # Pode ser em aberto
    valor_mensal          = models.DecimalField(max_digits=10, decimal_places=2)
    carga_horaria_semanal = models.IntegerField(help_text="Horas por semana")
    tipo_contrato         = models.CharField(
        max_length=50,
        choices=[
            ('PJ', 'Pessoa Jurídica'),
            ('Intermitente', 'Intermitente'),
            ('Freelancer', 'Freelancer'),
        ]
    )
    descricao_atividades  = models.TextField()
    ativo                 = models.BooleanField(default=True)
    criado_em             = models.DateTimeField(auto_now_add=True)
    atualizado_em         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato de {self.motoboy.nome_completo} - {self.tipo_contrato}"
    
class Contrato_Item(models.Model):
    TIPO_DADO_CHOICES = [
        ('boolean', 'Booleano'),
        ('integer', 'Inteiro'),
        ('string', 'Texto'),
        ('float', 'Decimal'),
    ]

    nome          = models.CharField(max_length=100)
    chave_sistema = models.SlugField(unique=True, help_text="Chave usada pelo sistema para leitura do item")
    tipo_dado     = models.CharField(max_length=10, choices=TIPO_DADO_CHOICES)
    valor_padrao  = models.CharField(max_length=100, blank=True, null=True)
    obrigatorio   = models.BooleanField(default=False)

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

class Estabelecimento_Contrato(models.Model):
    estabelecimento    = models.OneToOneField(Estabelecimento, on_delete=models.CASCADE)  # MUDANÇA AQUI
    data_inicio        = models.DateField(null=True, blank=True)
    data_fim           = models.DateField(null=True, blank=True)
    status             = models.CharField(
        max_length=20,
        choices=[
            ("vigente", "Vigente"),
            ("vencido", "Vencido"),
            ("encerrada", "Encerrada"),
            ("bloqueado", "Bloqueado")
        ],
        default="vigente"
    )

    def __str__(self):
        return f'{self.estabelecimento.nome} '

class Estabelecimento_Contrato_Item(models.Model):
    contrato  = models.ForeignKey(Estabelecimento_Contrato, on_delete=models.CASCADE, related_name='itens')
    item      = models.ForeignKey(Contrato_Item, on_delete=models.CASCADE)
    valor     = models.CharField(max_length=100)

    class Meta:
        unique_together = ('contrato', 'item')

    def __str__(self):
        return f"{self.item.nome} = {self.valor}" 

class Estabelecimento_Fatura(models.Model):
    estabelecimento      = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    data_referencia      = models.DateField()
    valor_total          = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_alocacoes = models.PositiveIntegerField(default=0)  
    status               = models.CharField(
        max_length=20,
        choices=[("aberta", "Aberta"), ("paga", "Paga"), ("vencida", "Vencida")],
        default="aberta"
    )
    gerada_em            = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Fatura - ({self.estabelecimento.nome}) {self.data_referencia.strftime("%m/%Y")}'

class Vaga(models.Model):
    TIPO_VAGA_CHOICES = [
        ('fixa', 'Fixa'),
        ('spot', 'Spot'),
    ]

    id                    = models.AutoField(primary_key=True)
    contrato              = models.ForeignKey(Estabelecimento_Contrato, on_delete=models.CASCADE, null=True, blank=True)
    tipo_vaga             = models.CharField(max_length=10, choices=TIPO_VAGA_CHOICES,  blank=True,    null=True,)
    observacao            = models.CharField(max_length=300, null=True, blank=True)
    data_da_vaga          = models.DateField(null=True, blank=True)
    hora_inicio_padrao    = models.TimeField(default='00:00')
    hora_fim_padrao       = models.TimeField(default='00:00')
    status                = models.CharField(
        max_length=20,
        choices=[
            ("aberta", "Aberta"),
            ("reservada", "Reservada"),
            ("finalizada", "Finalizada"),
            ("cancelada", "Cancelada")
        ],
        default="aberta"
    )
    def __str__(self):
        return (
        f"Vaga {self.id} - "
        f"{self.contrato.estabelecimento.nome if self.contrato and self.contrato.estabelecimento else 'Sem estabelecimento'} | "
        f"Data: {self.data_da_vaga.strftime('%d/%m/%Y') if self.data_da_vaga else 'Sem data'} | "
        f"Status: {self.get_status_display()}"
    )

class Supervisor_Motoboy(models.Model):
    supervisor  = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    motoboy     = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('supervisor', 'motoboy')
    
    def __str__(self):
        return f"Supervisor {self.supervisor.nome} - Motoboy {self.motoboy.nome}"

class Supervisor_Estabelecimento(models.Model):
    supervisor      = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('supervisor', 'estabelecimento')
    
    def __str__(self):
        return f"Supervisor {self.supervisor.nome} - Estabelecimento {self.estabelecimento.nome}"

class Motoboy_Alocacao(models.Model):
    vaga                = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    motoboy             = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    entregas_realizadas = models.PositiveIntegerField(default=0)
    status              = models.CharField(
        max_length=20,
        choices=[('livre', 'Livre'), ('alocado', 'Alocado')],
        default='livre'
    )
    class Meta:
        unique_together = ('motoboy', 'vaga')

    def __str__(self):
        return f"{self.motoboy.nome} - {self.status}"

class Motoboy_Candidatura(models.Model):
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
class Motoboy_Ranking(models.Model):
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











