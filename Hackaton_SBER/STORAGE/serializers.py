from rest_framework import serializers
from .models import ApplicationBase, CreditHistoryReport, ObligationInformation


class CreditHistoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditHistoryReport
        fields = '__all__'

class ObligationInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObligationInformation
        fields = '__all__'
class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBase
        fields = '__all__'

