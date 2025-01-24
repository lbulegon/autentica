
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
