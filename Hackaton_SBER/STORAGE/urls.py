from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import *

router_application = SimpleRouter()
router_application.register(r'applicationlist', ApplictionCRUD)


urlpatterns = [
    path('api/', include(router_application.urls)),
    # http://127.0.0.1:8000/api/v1/resumelist/ (<int:pk>/) запись по своему id

]