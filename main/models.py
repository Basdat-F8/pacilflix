from django.db import models
import uuid

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