from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import *

router_application = SimpleRouter()
router_application.register(r'applicationlist', ApplictionCRUD)


router_credit_history_reports = SimpleRouter()
router_credit_history_reports.register(r'credithistorylist', CreditHistoryReportsCRUD)

router_obligation_info = SimpleRouter()
router_obligation_info.register(r'obligationinfolist', ObligationInfoCRUD)

router_bank_deposit = SimpleRouter()
router_bank_deposit.register(r'bankdepositlist', BankDepositCRUD)

router_requested_condition = SimpleRouter()
router_requested_condition.register(r'requestedconditionlist', RequestedConditionsCRUD)


urlpatterns = [
    path('api/', include(router_application.urls)),
    # http://127.0.0.1:8000/api/application/ (<int:pk>/) запись по своему id
    path('api/', include(router_credit_history_reports.urls)),
    path('api/', include(router_obligation_info.urls)),
    path('api/', include(router_bank_deposit.urls)),
    path('api/', include(router_requested_condition.urls)),

    path('api/application-with-related-data/<int:pk>/', ApplicationWithRelatedData.as_view(), name='application-with-related-data'),
    path('api/obligationinfolist/byapplicationid/<int:application_id>/', ObligationInfoCRUD.as_view({'get': 'byapplicationid'})),

]