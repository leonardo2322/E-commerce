from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Cuando un usuario es creado, crea el perfil asociado
    if created:
        print(f"Creating profile for user: {instance.username}")
        Profile.objects.get_or_create(user=instance, email=instance.email)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()