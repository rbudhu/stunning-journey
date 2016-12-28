from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        widgets = {'box': forms.HiddenInput()}
        fields = ('image', 'text', 'box', 'num_panels', 'text_pos', 'share', )
        labels = {
            'text': 'Text',
            'image': 'Image',
            'num_panels': 'Number of Panels',
            'text_pos': 'Text Position'
        }
