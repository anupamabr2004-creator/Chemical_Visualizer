# equipment/serializers.py
from rest_framework import serializers
from .models import Dataset
from django.contrib.auth.models import User

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'total_equipment', 'average_flowrate', 'average_pressure', 'average_temperature', 'type_distribution']
        read_only_fields = ['id', 'uploaded_at']