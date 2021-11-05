from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class ShortenURL(models.Model):
    """ Table that stores the original URL """
    id = models.BigIntegerField(
        primary_key=True, validators=[
            # maximum value that can be represented by 8 digit base62 string
            MaxValueValidator(62**8-1),
            MinValueValidator(1_000_000)
        ]
    )
    url = models.URLField(unique=True, max_length=1000)

    def __str__(self) -> str:
        return f"({self.id}, {self.url})"

    # functions that uses ShortenURL.save() should handle ValidationError
    def save(self, *args, **kwargs):
        self.id = ShortenURL.objects.last().id + 1 \
            if ShortenURL.objects.count() \
            else 1_000_000     # id starts from 10M
        self.full_clean()
        super().save(*args, **kwargs)
