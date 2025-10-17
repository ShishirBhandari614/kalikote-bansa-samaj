from django import forms
from .models import Notices

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['name', 'file']
