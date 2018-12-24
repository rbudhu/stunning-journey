import io
import json
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.html import mark_safe

from PIL import Image

from .tenso import Tenso

# Create your models here.
class Document(models.Model):
    TEXT_POS_CHOICES = (
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        )

    text = models.CharField(max_length=20, blank=True)
    # TODO: Remove blank=True when cropper is re-implemented
    box = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='.')
    num_panels = models.IntegerField()
    text_pos = models.CharField(max_length=10, choices=TEXT_POS_CHOICES,
                                default='Top')
    share = models.BooleanField(default=False)
    gif = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            img = Image.open(io.BytesIO(self.image.read()))
            tenso = Tenso(img, json.loads(self.box),
                          num_panels = self.num_panels,
                          text = self.text,
                          text_pos = self.text_pos,
                          font_path=settings.FONT_PATH)
            buffer = io.BytesIO()
            if self.gif is True:
                frames = tenso.generate_gif()
                frames[0].save(buffer, save_all=True,
                               append_images=frames[1:],
                               duration=800,
                               loop=0,
                               format='GIF')
                buffer.seek(0)
                self.image = InMemoryUploadedFile(buffer, 'ImageField',
                                                  self.image.name, 'image/gif',
                                                  buffer.getbuffer().nbytes,
                                                  None, None)
            else:
                tenso.generate().save(buffer, format='JPEG')
                buffer.seek(0)
                self.image = InMemoryUploadedFile(buffer, 'ImageField',
                                                  self.image.name, 'image/jpeg',
                                                  buffer.getbuffer().nbytes,
                                                  None, None)
        return super(Document, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe('<img src="{}{}" width="150" height="350" title="Tenso"/>'.format(settings.MEDIA_URL, self.image))

    def __str__(self):
        return 'Document {} - {}'.format(self.pk, self.created)

    image_tag.short_description = 'Tenso Meme'
