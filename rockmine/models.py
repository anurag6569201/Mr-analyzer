from django.db import models

class DataUploadModel(models.Model):
    data = models.TextField()