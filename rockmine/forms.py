from django import forms
from .models import DataUploadModel

class DataUploadForm(forms.ModelForm):
    class Meta:
        model = DataUploadModel
        fields = ['data']

    def clean_data(self):
        data = self.cleaned_data['data']
        try:
            data_list = [float(i) for i in data.split(',')]
        except ValueError:
            raise forms.ValidationError("Invalid data format. Please enter a comma-separated list of numbers.")
        return data
