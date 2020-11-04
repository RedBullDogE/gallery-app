from django.db import models
from django.contrib.auth import get_user_model


class Picture(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pictures'
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        blank=True
    )
    date = models.DateField(
        auto_now_add=True
    )
    file = models.ImageField(
        upload_to='pictures'
    )
