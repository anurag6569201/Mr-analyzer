from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size(value):
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb}MB")

class PDFDocument(models.Model):
    pdf_file = models.FileField(
        upload_to='pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_file_size]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name
