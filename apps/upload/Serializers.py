
from rest_framework import serializers
from .models import Csv


class CSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Csv
        fields = ['id', 'file_name', 'uploaded', 'activated']