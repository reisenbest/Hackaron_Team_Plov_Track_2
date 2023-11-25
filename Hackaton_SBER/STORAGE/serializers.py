from rest_framework import serializers
from .models import ApplicationBase, CreditHistoryReport, ObligationInformation, BankDeposit, RequestedConditions, DocumentPackage


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

class BankDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDeposit
        fields = '__all__'

class RequestedConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedConditions
        fields = '__all__'

class DocumentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentPackage
        fields = '__all__'


