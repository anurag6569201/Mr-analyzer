from django.db import models

class top10alltime(models.Model):
    image_path=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    overview=models.CharField(max_length=500)
    released_date=models.DateField()
    runtime=models.IntegerField(default=0)
    
