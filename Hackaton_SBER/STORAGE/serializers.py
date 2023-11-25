from rest_framework import serializers
from .models import ApplicationBase, CreditHistoryReport


class CreditHistoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditHistoryReport
        fields = '__all__'
class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBase
        fields = '__all__'

