from django import forms
from .models import DiseaseNameModel

class DiseaseNameForm(forms.ModelForm):
    class Meta:
        model=DiseaseNameModel
        fields=['name','nos']