from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    fields = ( 'image_tag', 'text', 'box', 'image', 'num_panels',
               'share', 'text_pos', )
    readonly_fields = ('image_tag',)
    
admin.site.register(Document, DocumentAdmin)
# Register your models here.
