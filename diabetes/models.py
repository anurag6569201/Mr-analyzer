from django.db import models

class DataUploadModel(models.Model):
    pregnancies = models.IntegerField()
    glucose = models.IntegerField()
    blood_pressure = models.IntegerField()
    insulin = models.IntegerField()
    bmi = models.FloatField()
    dbf = models.FloatField()
    age = models.IntegerField()