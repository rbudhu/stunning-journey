from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    num_panels = forms.IntegerField(
        initial = 4, min_value = 2,
        max_value = 6, label = 'Number of Panels (optional)')

    class Meta:
        model = Document
        widgets = {'box': forms.HiddenInput()}
        fields = ('image', 'text', 'text_pos', 'box', 'num_panels',)
        labels = {
            'text': 'Text (20 chars max - optional)',
            'image': 'Image',
            'text_pos': 'Text Position (optional)',
            'num_panels': 'Number of Panels (optional)',
        }
