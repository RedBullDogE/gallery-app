from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path

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

    thumbnail = models.ImageField(
        upload_to='pictures/thumbs',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Picture, self).save(*args, **kwargs)

        if is_new:
            # Resizing image if it is larger than 1080x1080
            img = Image.open(self.file.path)
            if img.height > 1080 or img.width > 1080:
                new_size = (1080, 1080)
                img.thumbnail(new_size, Image.ANTIALIAS)
                img.save(self.file.path)

            # Creating thumbnail
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

            super(Picture, self).save(*args, **kwargs)
    

    def make_thumbnail(self):
        thumb_size = (512, 512)
        image = Image.open(self.file)
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        thumb_extension = Path(self.file.name).suffix.lower()
        thumb_name = Path(self.file.name).stem

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        print(thumb_filename)

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
            

    class Meta:
        ordering = ['-pub_date']

