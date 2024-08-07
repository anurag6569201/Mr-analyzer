from django import forms
from .models import DataUploadModel

class DataUploadForm(forms.ModelForm):
    class Meta:
        model = DataUploadModel
        fields = ['pregnancies','glucose','blood_pressure','skin_thickness','insulin','bmi','dbf','age']
