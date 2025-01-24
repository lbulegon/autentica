
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime

def validate_nota(value):
    if value < 0 or value > 9:
        raise ValidationError('A nota deve estar entre 0 e 9.')


class estado(models.Model):
    estado_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome
class cidade(models.Model):
    
    nome         = models.CharField(max_length=255)
    estado_id    = models.ForeignKey(estado, on_delete=models.CASCADE)
    codigo_ibge  = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome


class bairro(models.Model):
    id = models.IntegerField(primary_key=True)  # Sem `primary_key=True`
    nome = models.CharField(max_length=255)
    cidade = models.ForeignKey('cidade', on_delete=models.CASCADE)

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
    estado_id          = models.ForeignKey(estado, on_delete=models.PROTECT)
    cidade_id          = models.ForeignKey(cidade, on_delete=models.PROTECT)
   # bairro_id          = models.ForeignKey(bairro, on_delete=models.PROTECT)
    
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

class supervisor(models.Model):
    id                 = models.AutoField(primary_key=True)
    nome               = models.CharField(max_length=255, null=False, blank=False)
    cep                = models.CharField(max_length=10)
    estado_id          = models.ForeignKey(estado, on_delete=models.PROTECT)
    cidade_id          = models.ForeignKey(cidade, on_delete=models.PROTECT)
 #   bairro_id          = models.ForeignKey(bairro, on_delete=models.PROTECT)
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

class empresa(models.Model):
    id                 = models.AutoField(primary_key=True)
    nome               = models.CharField(max_length=255, null=False, blank=False)
    cep                = models.CharField(max_length=10)
    estado_id          = models.ForeignKey(estado, on_delete=models.PROTECT)
    cidade_id          = models.ForeignKey(cidade, on_delete=models.PROTECT)
    bairro_id          = models.ForeignKey(bairro, on_delete=models.PROTECT)
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
    empresa_id    = models.ForeignKey(empresa, on_delete=models.PROTECT, related_name='pedidos')
    motoboy_id    = models.OneToOneField(motoboy, on_delete=models.PROTECT, null=True, blank=True, related_name='vaga')  # O campo pode ser NULL e deixado em branco
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


class avaliacao(models.Model):
    AVALIADO_CHOICES = (
        ('motoboy', 'Motoboy'),
        ('empresa', 'Empresa'),
        ('supervisor', 'Supervisor'),
        ('superuser', 'Super usuario'),
    )

    avaliado_tipo  = models.CharField(max_length=10, choices=AVALIADO_CHOICES)
    avaliado_id    = models.IntegerField()  # Armazena o ID do Motoboy, Empresa ou Supervisor
    avaliador      = models.ForeignKey(User, on_delete=models.CASCADE)  # Quem fez a avaliação
    nota           = models.PositiveSmallIntegerField(validators=[validate_nota])  # Restringe de 0 a 9
    comentario     = models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)


    avaliador   =   models.CharField(
        max_length=20,
        choices=[
           ('motoboy', 'Motoboy'),
           ('empresa', 'Empresa'),
           ('supervisor', 'Supervisor'),
           ('superuser', 'Super usuario'),
        ],
        default="superuser"
    )

    def __str__(self):
        return f"{self.avaliado_tipo} - Nota: {self.nota}"
class avaliacaomotoboy(models.Model):
    motoboy        = models.ForeignKey(motoboy, on_delete=models.CASCADE, related_name='avaliacoes')
   # avaliador      = models.ForeignKey(User, on_delete=models.CASCADE)
    nota           = models.PositiveSmallIntegerField(validators=[validate_nota])  # Restringe de 0 a 9
    comentario     = models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

class avaliacaoempresa(models.Model):
    empresa        = models.ForeignKey(empresa, on_delete=models.CASCADE, related_name='avaliacoes')
  #  avaliador      = models.ForeignKey(User, on_delete=models.CASCADE)
    nota           = models.PositiveSmallIntegerField(validators=[validate_nota])  # Restringe de 0 a 9
    comentario     = models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)


class avaliacaosupervisor(models.Model):
    supervisor     = models.ForeignKey(supervisor, on_delete=models.CASCADE, related_name='avaliacoes')
 #   avaliador      = models.ForeignKey(User, on_delete=models.CASCADE)
    nota           = models.PositiveSmallIntegerField(validators=[validate_nota])  # Restringe de 0 a 9
    comentario     = models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)


class contratoempresa(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('encerrado', 'Encerrado'),
        ('pendente', 'Pendente'),
    )

    id              = models.AutoField(primary_key=True)
    empresa         = models.ForeignKey(empresa, on_delete=models.PROTECT, related_name='contratos_empresa')
    valor           = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do contrato com a empresa
    data_inicio     = models.DateField()  # Data de início do contrato
    data_termino    = models.DateField()  # Data de término do contrato
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    observacoes     = models.TextField(null=True, blank=True)  # Campo para observações adicionais
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato Empresa {self.id} - {self.empresa.nome} - Status: {self.get_status_display()}"

    def clean(self):
        if self.data_termino <= self.data_inicio:
            raise ValidationError("A data de término deve ser posterior à data de início.")

    class Meta:
        verbose_name_plural = "Contratos de Empresa"


class contratomotoboy(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('encerrado', 'Encerrado'),
        ('pendente', 'Pendente'),
    )

    id              = models.AutoField(primary_key=True)
    motoboy         = models.ForeignKey(motoboy, on_delete=models.PROTECT, related_name='contratos_motoboy')
    valor           = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do contrato com o motoboy
    data_inicio     = models.DateField()  # Data de início do contrato
    data_termino    = models.DateField()  # Data de término do contrato
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    observacoes     = models.TextField(null=True, blank=True)  # Campo para observações adicionais
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato Motoboy {self.id} - {self.motoboy.nome} - Status: {self.get_status_display()}"

    def clean(self):
        if self.data_termino <= self.data_inicio:
            raise ValidationError("A data de término deve ser posterior à data de início.")

    class Meta:
        verbose_name_plural = "Contratos de Motoboy"

class categoria(models.Model):
    nome      = models.CharField(max_length=50, unique=True)  # Nome da categoria, ex: 'Iniciante', 'Bronze'
    descricao = models.TextField(help_text="Descrição da categoria")  # Descrição opcional para a categoria

    def __str__(self):
        return self.nome


class categoriamotoboy(models.Model):
    motoboy                    = models.ForeignKey(motoboy, on_delete=models.CASCADE, related_name="categorias")  # Relacionamento com a tabela Motoboy
    categoria                  = models.ForeignKey(categoria, on_delete=models.CASCADE, related_name="criterios")  # Relacionamento com a tabela Categoria
    pontualidade_minima        = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentual mínimo de pontualidade, ex: 70%")
    taxa_aceitacao_minima      = models.DecimalField(max_digits=5, decimal_places=2, help_text="Taxa mínima de aceitação, ex: 60%")
    taxa_cancelamento_maxima   = models.DecimalField(max_digits=5, decimal_places=2, help_text="Taxa máxima de cancelamento, ex: 10%")
    frequencia_uso_minima      = models.IntegerField(help_text="Dias mínimos de uso nos últimos 30 dias")
    entregas_concluidas_minima = models.IntegerField(help_text="Número mínimo de entregas concluídas")

    def __str__(self):
        return f"{self.motoboy.nome} - Categoria: {self.categoria.nome}"


class emprestimo(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('quitado', 'Quitado'),
        ('inadimplente', 'Inadimplente'),
    )

    motoboy         = models.ForeignKey(motoboy, on_delete=models.PROTECT, related_name='emprestimos')
    valor_total     = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor total do empréstimo")
    numero_parcelas = models.PositiveIntegerField(help_text="Número de parcelas")
    juros_mensal    = models.DecimalField(max_digits=5, decimal_places=2, help_text="Taxa de juros mensal em %")
    data_inicio     = models.DateField( help_text="Data de início do empréstimo")
    status          = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativo')
    observacoes     = models.TextField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Empréstimo {self.id} - {self.motoboy.nome} - Status: {self.get_status_display()}"

    def clean(self):
        if self.numero_parcelas <= 0:
            raise ValidationError("O número de parcelas deve ser maior que zero.")

class parcelaemprestimo(models.Model):
    emprestimo      = models.ForeignKey(emprestimo, on_delete=models.CASCADE, related_name='parcelas')
    numero_parcela  = models.PositiveIntegerField(help_text="Número da parcela")
    valor_parcela   = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor da parcela")
    data_vencimento = models.DateField(help_text="Data de vencimento da parcela")
    data_pagamento  = models.DateField(null=True, blank=True, help_text="Data em que a parcela foi paga")
    status          = models.CharField(max_length=10, choices=(('pago', 'Pago'), ('pendente', 'Pendente')), default='pendente')

    def __str__(self):
        return f"Parcela {self.numero_parcela} - Empréstimo {self.emprestimo.id} - Status: {self.get_status_display()}"

    def clean(self):
        if self.data_pagamento and self.data_pagamento < self.data_vencimento:
            raise ValidationError("A data de pagamento não pode ser anterior à data de vencimento.")