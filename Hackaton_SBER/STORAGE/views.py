from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from .serializers import ApplicationBaseSerializer

from .models import ApplicationBase

@extend_schema(description="Application URLs:", tags=["Application"])
class ApplictionCRUD(viewsets.ModelViewSet):
    queryset = ApplicationBase.objects.all()
    serializer_class = ApplicationBaseSerializer
    lookup_field = 'pk'