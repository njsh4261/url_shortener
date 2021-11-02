from django.core.checks import messages
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.core.exceptions import ValidationError
from .constants import *

# Create your models here.
class ShortenURL(models.Model):
    id = models.BigIntegerField(
        primary_key=True, validators=[
            MaxValueValidator(62**8-1, message=VALID_ERR_MSG_MAX),     # maximum value that can be represented by 8 digit base62 string
            MinValueValidator(1_000_000, message=VALID_ERR_MSG_MIN)
        ]
    )
    url = models.URLField(unique=True, max_length=1000)

    def __str__(self) -> str:
        return "({0}, {1})".format(self.id, self.url)

    # functions that uses ShortenURL.save() should handle ValidationError
    def save(self, *args, **kwargs):        # id starts from 1M
        self.id = ShortenURL.objects.last().id + 1 \
            if ShortenURL.objects.count() \
            else 1_000_000
        self.full_clean()
        super().save(*args, **kwargs)
