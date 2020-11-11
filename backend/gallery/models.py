from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image


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
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    file = models.ImageField(
        upload_to='pictures'
    )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Picture, self).save(*args, **kwargs)

        if is_new:
            img = Image.open(self.file.path)
            if img.height > 1080 or img.width > 1080:
                new_size = (1080, 1080)
                img.thumbnail(new_size)
                img.save(self.file.path)

    class Meta:
        ordering = ['-pub_date']

