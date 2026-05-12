from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    is_online = models.BooleanField(
            default=False,
            null=False,
            )
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name='Perfil',
            unique=True,
            )
    created = models.DateTimeField(
            auto_now_add=True,
            verbose_name="Data de criação",
            )
    nickname = models.CharField(
            max_length=32,
            blank=True,  # Optional
            null=True,
            unique=True,
            verbose_name="Apelido",
            )
    profile_picture = models.ImageField(
            blank=True,  # Optional
            null=True,
            upload_to='media/profile_picture/',
            verbose_name="Foto do usuário",
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Saves image as it is first

        if self.profile_picture: # Avoid trying to resize photo when deleting it
            img = Image.open(self.profile_picture.path)
            if img.height > 100 or img.width > 100:
                new_img = (100, 100)
                img.thumbnail(new_img, Image.LANCZOS)
                img.save(self.profile_picture.path, optimize=True)  # Save new image in same path

    class Meta:
        verbose_name = 'Perfis'
        verbose_name_plural = 'Perfil'

    def __str__(self):
        if self.nickname:
            return f"{self.user.username} - {self.nickname}"
        return f"{self.user.username}"


# Auto create new 'Profile' instance when new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
                user=instance,
                is_online=True
                )
