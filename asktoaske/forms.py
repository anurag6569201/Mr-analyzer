from django import forms
from .models import PDFDocument

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['pdf_file']