from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import  AbstractUser
from phonenumber_field.modelfields import PhoneNumberField



# Create your models here.





class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=False, blank=True, null=True)
    phone_number = PhoneNumberField(blank=False, unique=True, null=False)
    phone_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username



class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    longitude = models.FloatField()
    lattitude = models.FloatField()
    phone_number = models.CharField(max_length=50)
    website = models.CharField(max_length=150, default='https://megasaver.com/')

    def __str__(self) -> str:
        return self.name
   
    


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)