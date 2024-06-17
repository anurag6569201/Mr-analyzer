from django import forms
from .models import DataUploadModel

class DataUploadForm(forms.ModelForm):
    class Meta:
        model = DataUploadModel
        fields = ['text']
