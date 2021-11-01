from django.db import models
from django.db.models.base import Model

# Create your models here.
class ShortenURL(models.Model):
    url = models.URLField(max_length=1000)
