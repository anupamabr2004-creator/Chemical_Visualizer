from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets', null=True, blank=True)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_equipment = models.IntegerField()
    average_flowrate = models.FloatField()
    average_pressure = models.FloatField()
    average_temperature = models.FloatField()

    type_distribution = models.JSONField()

    def __str__(self):
        return self.filename

