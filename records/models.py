
from django.db import models
class Record(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    description=models.TextField()
    class Meta:
        unique_together=('name','email')
