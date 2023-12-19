from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import  AbstractUser
from phonenumber_field.modelfields import PhoneNumberField






class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=False, blank=True, null=True)
    phone_number = PhoneNumberField(blank=False, unique=True, null=False)
    phone_verified = models.BooleanField(default=False)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    requesting_a_ride = models.CharField(max_length=30, null=True, blank=True)
    giving_a_ride_to = models.CharField(max_length=30, null=True, blank=True)
    is_driver = models.BooleanField(default=False) 

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.username}"




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)