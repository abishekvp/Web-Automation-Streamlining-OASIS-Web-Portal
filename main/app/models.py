from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=32)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    
class message(models.Model):
    msg = models.CharField(max_length=200)

