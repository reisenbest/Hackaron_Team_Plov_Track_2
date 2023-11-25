from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import *

router_application = SimpleRouter()
router_application.register(r'applicationlist', ApplictionCRUD)


router_credit_history_reports = SimpleRouter()
router_credit_history_reports.register(r'credithistorylist', CreditHistoryReportsCRUD)

urlpatterns = [
    path('api/', include(router_application.urls)),
    # http://127.0.0.1:8000/api/application/ (<int:pk>/) запись по своему id
    path('api/', include(router_credit_history_reports.urls)),

path('api/application-with-related-data/<int:pk>/', ApplicationWithRelatedData.as_view(), name='application-with-related-data'),
]