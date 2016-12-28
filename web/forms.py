from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    num_panels = forms.IntegerField(min_value = 2, max_value = 6,
                                    label = 'Number of Panels')

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
