from rest_framework import serializers
from .models import ApplicationBase

class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBase
        fields = '__all__'

