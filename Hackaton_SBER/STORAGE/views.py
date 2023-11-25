from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import ApplicationBaseSerializer, CreditHistoryReportSerializer, ObligationInformationSerializer, BankDepositSerializer, RequestedConditionsSerializer, DocumentPackageSerializer

from .models import ApplicationBase, CreditHistoryReport, ObligationInformation, BankDeposit, RequestedConditions, DocumentPackage

@extend_schema(description="все заявки или одельную заявку по id", tags=["Application"])
class ApplictionCRUD(viewsets.ModelViewSet):
    queryset = ApplicationBase.objects.all()
    serializer_class = ApplicationBaseSerializer
    lookup_field = 'pk'

    @action(detail=True, url_path='credithistorylist', serializer_class=CreditHistoryReportSerializer)
    def credithistorylist(self, request, pk=None):
        application = self.get_object()
        credit_history_list = CreditHistoryReport.objects.filter(application=application)
        serializer = CreditHistoryReportSerializer(credit_history_list, many=True)
        return Response(serializer.data)

@extend_schema(description="получить все БИК, или получить конкретный БИК по id связанной с ней заявки", tags=["CreditHistoryReports"])
class CreditHistoryReportsCRUD(viewsets.ModelViewSet):
    queryset = CreditHistoryReport.objects.all()
    serializer_class = CreditHistoryReportSerializer
    lookup_field = 'application_id'


@extend_schema(description="Информация об обязательствах. Кредитная история. получить все>", tags=["ObligationInfo"])
class ObligationInfoCRUD(viewsets.ModelViewSet):
    queryset = ObligationInformation.objects.all()
    serializer_class = ObligationInformationSerializer
    lookup_field = 'pk'

    @action(detail=False, methods=['get'], )
    def byapplicationid(self, request, application_id=None):

        # получаем все записи которые есть для указанного application_id
        if application_id is None:
            return Response({"error": "введите application_id."}, status=status.HTTP_400_BAD_REQUEST)

        if application_id not in ObligationInformation.objects.values_list('application', flat=True):
            return Response({"error": "записи с таким application_id не существует"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = ObligationInformation.objects.filter(application_id=application_id)
        serializer = ObligationInformationSerializer(queryset, many=True)

        return Response(serializer.data)

@extend_schema(description="Наличие сбережений на счетах в Банке", tags=["BankDeposit"])
class BankDepositCRUD(viewsets.ModelViewSet):
    queryset = BankDeposit.objects.all()
    serializer_class = BankDepositSerializer
    lookup_field = 'application_id'

@extend_schema(description="Запрашиваемые и предлагаемые банком условия по конкретной кредитной заявке", tags=["RequestedConditions"])
class RequestedConditionsCRUD(viewsets.ModelViewSet):
    queryset = RequestedConditions.objects.all()
    serializer_class = RequestedConditionsSerializer
    lookup_field = 'application_id'
@extend_schema(description="Пакет документов", tags=["DocumentPackage"])
class DocumentPackageViewSet(viewsets.ModelViewSet):
    queryset = DocumentPackage.objects.all()
    serializer_class = DocumentPackageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], )
    def byapplicationid(self, request, application_id=None):

        # получаем все записи которые есть для указанного application_id
        if application_id is None:
            return Response({"error": "введите application_id."}, status=status.HTTP_400_BAD_REQUEST)

        if application_id not in DocumentPackage.objects.values_list('application', flat=True):
            return Response({"error": "записи с таким application_id не существует"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = DocumentPackage.objects.filter(application_id=application_id)
        serializer = DocumentPackageSerializer(queryset, many=True)

        return Response(serializer.data)


@extend_schema(description="Получить кредитную заявку по id и ВСЮ (документы, отчет БИК и т.д) связанную с ней инфу", tags=["GetFullApplication"])
class ApplicationWithRelatedData(APIView):
    def get(self, request, pk):
        application = ApplicationBase.objects.get(pk=pk)
        application_serializer = ApplicationBaseSerializer(application).data

        credit_history_list = CreditHistoryReport.objects.filter(application=application)
        credit_history_serializer = CreditHistoryReportSerializer(credit_history_list, many=True).data

        obligation_info_list = ObligationInformation.objects.filter(application=application)
        obligation_info_serializer = ObligationInformationSerializer(obligation_info_list, many=True).data

        bank_deposit_list = BankDeposit.objects.filter(application=application)
        bank_deposit_serializer = BankDepositSerializer(bank_deposit_list, many=True).data

        requested_condition_list = RequestedConditions.objects.filter(application=application)
        requested_condition_serializer = RequestedConditionsSerializer(requested_condition_list, many=True).data

        document_package_list = DocumentPackage.objects.filter(application=application)
        document_package_serializer = DocumentPackageSerializer(document_package_list, many=True).data

        response_data = {
            'application': application_serializer,
            'credit_history_list': credit_history_serializer,
            'obligation_info_list':obligation_info_serializer,
            'bank_deposit_list': bank_deposit_serializer,
            'requested_condition_list': requested_condition_serializer,
            'document_package_list': document_package_serializer
            # добавьте сюда другие связанные данные, если они есть
        }

        return Response(response_data)