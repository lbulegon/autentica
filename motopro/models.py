from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import re

from decimal import Decimal

from sympy import Sum

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


class Categoria_Desconto(models.Model):
    nome         = models.CharField(max_length=100, unique=True)
    descricao    = models.TextField(blank=True)
    ativo        = models.BooleanField(default=True)
    criado_em    = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

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

class Motoboy_Nivel(models.Model):
    nome      = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True)
    ordem     = models.PositiveIntegerField(unique=True)  # Para ordenação dos rankings

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['ordem']

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
    estabelecimento   = models.OneToOneField(Estabelecimento, on_delete=models.CASCADE)
    data_inicio       = models.DateField(null=True, blank=True)
    data_fim          = models.DateField(null=True, blank=True)
    valor_vaga_fixa   = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Valor da Vaga Fixa"    )
    valor_vaga_spot   = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Valor da Vaga Spot"    )
    valor_tele_extra   = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Valor da Tele Extra"    )
    status            = models.CharField(
        max_length=20,
        choices=[
            ("vigente", "Vigente"),
            ("vencido", "Vencido"),
            ("encerrada", "Encerrada"),
            ("bloqueado", "Bloqueado"),
        ],
        default="vigente"
    )

    def clean(self):
        chaves_obrigatorias_horarios = [
            "hora_inicio_dia",
            "hora_fim_dia",
            "hora_inicio_noite",
            "hora_fim_noite",
        ]

        erros = []

        if self.itens.filter(item__chave_sistema="permite_vaga_fixa").exists():
            chaves_fixas = ["max_vagas_fixas_dia", "max_vagas_fixas_noite"] + chaves_obrigatorias_horarios
            faltantes_fixas = [
                chave for chave in chaves_fixas
                if not self.itens.filter(item__chave_sistema=chave).exists()
            ]
            if faltantes_fixas:
                erros.append(f"Itens obrigatórios faltando para vagas fixas: {', '.join(faltantes_fixas)}")

        if self.itens.filter(item__chave_sistema="permite_vaga_spot").exists():
            faltantes_spot = [
                chave for chave in chaves_obrigatorias_horarios
                if not self.itens.filter(item__chave_sistema=chave).exists()
            ]
            if faltantes_spot:
                erros.append(f"Itens obrigatórios faltando para vaga spot: {', '.join(faltantes_spot)}")

        if erros:
            raise ValidationError(" | ".join(erros))

    def get_valor_item(self, chave):
        item = self.itens.filter(item__chave_sistema=chave).first()
        if item:
            return Decimal(item.valor)
    
        # fallback para campo direto
        if hasattr(self, chave):
            valor = getattr(self, chave)
            return valor if valor is not None else Decimal("0.00")
    
        return Decimal("0.00")


    def calcular_pagamentos(self, motoboy, data_inicio, data_fim):
        """
        Função para calcular os valores que o estabelecimento deve pagar
        e o valor que o motoboy deve receber durante um período específico.
        """
        # Verificar se o contrato está ativo
        if self.status != "vigente":
            return {"erro": "Contrato não está ativo para cálculo."}

        # Recuperar valores do contrato
        valor_fixa   = self.get_valor_item("valor_vaga_fixa")
        valor_spot   = self.get_valor_item("valor_vaga_spot")
        valor_extra  = self.get_valor_item("valor_tele_extra")

        # Calcular quantidade de vagas (fixas, spot e tele extra)
        vagas = motoboy.vagas.filter(data__range=(data_inicio, data_fim))

        total_fixas      = vagas.filter(tipo_vaga="fixa").count()
        total_spot       = vagas.filter(tipo_vaga="spot").count()
        total_extras     = vagas.filter(tipo_vaga="extra").count()

        # Calcular descontos
        total_descontos = motoboy.descontos.filter(
            data__range=(data_inicio, data_fim),
            ativo=True
        ).aggregate(total=Sum('valor'))['total'] or Decimal("0.00")

        # Cálculo total do pagamento para o estabelecimento
        total_estab_paga = (
            (total_fixas * valor_fixa) +
            (total_spot * valor_spot) +
            (total_extras * valor_extra)
        )

        # Cálculo total a ser recebido pelo motoboy
        total_motoboy_recebe = total_estab_paga - total_descontos

        return {
            "motoboy": motoboy.nome_completo,
            "estabelecimento": self.estabelecimento.nome,
            "período": f"{data_inicio} a {data_fim}",
            "vagas_fixas": total_fixas,
            "vagas_spot": total_spot,
            "teles_extra": total_extras,
            "valor_unit_fixa": valor_fixa,
            "valor_unit_spot": valor_spot,
            "valor_unit_extra": valor_extra,
            "total_estabelecimento_paga": total_estab_paga,
            "total_descontos": total_descontos,
            "total_motoboy_recebe": total_motoboy_recebe,
        }

    def __str__(self):
        return f'{self.estabelecimento.nome}'

class Estabelecimento_Contrato_Item(models.Model):
    contrato  = models.ForeignKey(Estabelecimento_Contrato, on_delete=models.CASCADE, related_name='itens')
    item      = models.ForeignKey(Contrato_Item, on_delete=models.CASCADE)
    valor     = models.CharField(max_length=100)

    class Meta:
        unique_together = ('contrato', 'item')

    def __str__(self):
        return f"{self.item.nome} = {self.valor}" 

class Estabelecimento_Fatura(models.Model):
    estabelecimento                 = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    data_referencia                 = models.DateField()
    valor_vaga_fixa                 = models.DecimalField(max_digits=10, decimal_places=2,  default=Decimal("0.00"))
    valor_tele_extra                = models.DecimalField(max_digits=10, decimal_places=2,  default=Decimal("0.00"))
    valor_vaga_spot                 = models.DecimalField(max_digits=10, decimal_places=2,  default=Decimal("0.00"))
    valor_total                     = models.DecimalField(max_digits=10, decimal_places=2,  default=Decimal("0.00"))
    quantidade_alocacoes            = models.PositiveIntegerField(default=0)  
    status                          = models.CharField(
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
        ('extra', 'Tele Extra'), #
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
            ("alocado", "Alocado"),
            ("finalizada", "Finalizada"), # finalizada mas não esta paga
            ("paga", "Paga"),             # Já foi faturada e o pagamento ja aconteceu
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

class Motoboy_Alocacao(models.Model):
    vaga                = models.OneToOneField(Vaga, on_delete=models.CASCADE)  # agora só permite uma alocação por vaga
    motoboy             = models.ForeignKey(Motoboy, on_delete=models.CASCADE)
    entregas_realizadas = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Atualiza o status da vaga para 'alocado'
        if self.vaga.status != 'alocado':
            self.vaga.status = 'alocado'
            self.vaga.save()

    def delete(self, *args, **kwargs):
        vaga = self.vaga  # guarda referência antes de deletar
        super().delete(*args, **kwargs)
        # Como só pode haver um motoboy, ao deletar volta para 'aberta'
        vaga.status = 'aberta'
        vaga.save()

    def __str__(self):
        return f"{self.motoboy.nome} alocado na Vaga {self.vaga.id}"

class Motoboy_BandaVaga(models.Model):
    alocacao = models.ForeignKey('Motoboy_Alocacao', on_delete=models.CASCADE, related_name='bandas')
    
    faixa_km = models.PositiveSmallIntegerField(choices=[
        (6, '6 km'),
        (7, '7 km'),
        (8, '8 km'),
        (9, '9 km'),
        (10, '10 km'),
        (11, '11 km'),
        (12, '12 km'),
        (13, '13 km'),
        (14, '14 km'),
        (15, '15 km'),
    ])
    quantidade = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('alocacao', 'faixa_km')

    def __str__(self):
        return f"{self.alocacao} - {self.faixa_km}km x{self.quantidade}"


class Motoboy_Adiantamento(models.Model):
    TIPO_ADIANTAMENTO_CHOICES = [
        ('adiantamento', ' Adiantamento'),
        ('fixo', 'Adiantamento Fixo'),
        ('bonus', 'Bônus'),
        ('ajuste', 'Ajuste Manual'),
        ('outro', 'Outro'),
    ]
    motoboy              = models.ForeignKey( Motoboy, on_delete=models.CASCADE, related_name='adiantamentos')
    data_referencia      = models.DateField(help_text="Data a que se refere o adiantamento (ex: dia do serviço)")
    data_pagamento       = models.DateField(auto_now_add=True)
    valor                = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tipo_adiantamento    = models.CharField(max_length=20, choices=TIPO_ADIANTAMENTO_CHOICES, default='adiantamento')
    observacao           = models.TextField(blank=True, null=True)
    criado_em            = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"{self.motoboy.nome} - {self.data_referencia.strftime('%d/%m/%Y')} - R$ {self.valor:.2f}"


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

class Motoboy_Desconto(models.Model):
    motoboy         = models.ForeignKey(Motoboy, on_delete=models.CASCADE, related_name='descontos')
    categoria       = models.ForeignKey(Categoria_Desconto, on_delete=models.PROTECT, related_name='descontos')
    data            = models.DateField()
    descricao       = models.TextField(help_text="Motivo do desconto ou observações")
    valor           = models.DecimalField(max_digits=10, decimal_places=2)
    aplicado_por    = models.CharField(max_length=100, help_text="Nome do responsável pelo desconto")
    ativo           = models.BooleanField(default=True)
    criado_em       = models.DateTimeField(auto_now_add=True)
    atualizado_em   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_desconto} - {self.motoboy.nome_completo} - R$ {self.valor:.2f}"

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











