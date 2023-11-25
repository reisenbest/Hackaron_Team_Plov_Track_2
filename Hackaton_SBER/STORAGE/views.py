from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from .serializers import ApplicationBaseSerializer, CreditHistoryReportSerializer

from .models import ApplicationBase, CreditHistoryReport

@extend_schema(description="все кредитные заявки или одельная заявка по id", tags=["Application"])
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

@extend_schema(description="все БИК,или конкретный БИК по id связанной с ней кредитной заявки заявки", tags=["CreditHistoryReports"])
class CreditHistoryReportsCRUD(viewsets.ModelViewSet):
    queryset = CreditHistoryReport.objects.all()
    serializer_class = CreditHistoryReportSerializer
    lookup_field = 'application_id'

@extend_schema(description="Получить кредитную заявку по id и ВСЮ (документы, отчет БИК и т.д) связанную с ней инфу", tags=["GetFullApplication"])
class ApplicationWithRelatedData(APIView):
    def get(self, request, pk):
        application = ApplicationBase.objects.get(pk=pk)
        application_serializer = ApplicationBaseSerializer(application).data

        credit_history_list = CreditHistoryReport.objects.filter(application=application)
        credit_history_serializer = CreditHistoryReportSerializer(credit_history_list, many=True).data

        response_data = {
            'application': application_serializer,
            'credit_history_list': credit_history_serializer,
            # добавьте сюда другие связанные данные, если они есть
        }

        return Response(response_data)
