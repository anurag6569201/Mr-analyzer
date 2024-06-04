from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    choosenoption=models.CharField(max_length=100)

    def __str__(self):
        return self.file.name