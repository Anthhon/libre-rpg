from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Campaign(models.Model):
    active = models.BooleanField(  # Used to deactive campaigns manually
            default=False,
            null=False,
            )
    created = models.DateTimeField(
            auto_now_add=True,
            verbose_name="Data de criação"
            )
    cover_image = models.ImageField(
            blank=True,  # Optional
            null=True,
            upload_to='media/campaign/cover/',
            verbose_name="Foto do usuário",
            )
    name = models.CharField(
            max_length=32,
            blank=False,
            null=True,
            unique=True,
            verbose_name="Nome da campanha",
            )
    description = models.CharField(
            max_length=128,
            blank=True,  # Optional
            null=True,
            unique=True,
            verbose_name="Descrição curta da campanha",
            )
    masters = models.ManyToManyField(
            User,
            blank=True,
            related_name='gmed_campaigns',
            verbose_name="Mestres",
            )
    players = models.ManyToManyField(
            User,
            blank=True,
            related_name='joined_campaigns',
            verbose_name="Jogadores",
            )


    class Meta:
        verbose_name = 'Campanhas'
        verbose_name_plural = 'Campanha'

    def __str__(self):
        if self.nickname:
            return f"{self.user.username} - {self.nickname}"
        return f"{self.user.username}"
