import io
import json
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from .tenso import Tenso

# Create your models here.
class Document(models.Model):
    TEXT_POS_CHOICES = (
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        )

    text = models.CharField(max_length=255, blank=True)
    # TODO: Remove blank=True when cropper is re-implemented
    box = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='.')
    num_panels = models.IntegerField(default=4)
    text_pos = models.CharField(max_length=10, choices=TEXT_POS_CHOICES,
                                default='Top')
    share = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        img = Image.open(io.BytesIO(self.image.read()))
        # TODO: Change hardcoded coordinates to self.box
        tenso = Tenso(img, json.loads(self.box),
                      num_panels = self.num_panels,
                      text = self.text,
                      text_pos = self.text_pos,
                      font_path=settings.FONT_PATH)
        buffer = io.BytesIO()
        tenso.generate().save(buffer, format='JPEG')
        # TODO: Sometime later, don't store the file -- upload to imgur
        buffer.seek(0)
        self.image = InMemoryUploadedFile(buffer, 'ImageField',
                                          self.image.name, 'image/jpeg',
                                          buffer.getbuffer().nbytes,
                                          None, None)
        return super(Document, self).save(*args, **kwargs)
