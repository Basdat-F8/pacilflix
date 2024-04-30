from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser

'''
class daftar_favorit(models.Model):
    judul = models.CharField(max_length=50) 
    username = models.CharField(max_length=50) # fk pengguna.username
    timestamp = models.DateTimeField()

class daftar_unduhan(models.Model):
    id_tayangan = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # fk tayangan.id
    username = models.CharField(max_length=50) # fk pengguna.username
    timestamp = models.DateTimeField()
'''

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    negara_asal = models.CharField(max_length=50, blank=False, null=False)
    USERNAME_FIELD = 'username'