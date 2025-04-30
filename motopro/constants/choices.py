from django.db import models

class MotoboyRanking(models.TextChoices):
    BRONZE = 'bronze', 'Bronze'
    PRATA = 'prata', 'Prata'
    OURO = 'ouro', 'Ouro'
    PLATINA = 'platina', 'Platina'
