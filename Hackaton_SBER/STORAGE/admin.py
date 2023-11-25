from django.contrib import admin

# Register your models here.

from .models import ApplicationBase, CreditHistoryReport
class ApplicationBaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ApplicationBase._meta.get_fields()]

class CreditHistoryReportAdmin (admin.ModelAdmin):
    list_display = [field.name for field in CreditHistoryReport._meta.get_fields()]

admin.site.register(ApplicationBase, ApplicationBaseAdmin)
admin.site.register(CreditHistoryReport, CreditHistoryReportAdmin)