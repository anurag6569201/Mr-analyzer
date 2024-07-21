from django.db import models

class DiseaseNameModel(models.Model):
    name=models.CharField(max_length=60)