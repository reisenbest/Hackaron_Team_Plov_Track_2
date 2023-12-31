from django.contrib import admin

# Register your models here.

from .models import ApplicationBase, CreditHistoryReport, ObligationInformation, BankDeposit, RequestedConditions, DocumentPackage
class ApplicationBaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ApplicationBase._meta.get_fields()]

class CreditHistoryReportAdmin (admin.ModelAdmin):
    list_display = [field.name for field in CreditHistoryReport._meta.get_fields()]

class ObligationInformationAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ObligationInformation._meta.get_fields()]

class BankDepositAdmin (admin.ModelAdmin):
    list_display = [field.name for field in BankDeposit._meta.get_fields()]

class RequestedConditionsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RequestedConditions._meta.get_fields()]

class DocumentPackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DocumentPackage._meta.get_fields()]

admin.site.register(ApplicationBase, ApplicationBaseAdmin)
admin.site.register(CreditHistoryReport, CreditHistoryReportAdmin)
admin.site.register(ObligationInformation, ObligationInformationAdmin)
admin.site.register(BankDeposit, BankDepositAdmin)
admin.site.register(RequestedConditions, RequestedConditionsAdmin)
admin.site.register(DocumentPackage, DocumentPackageAdmin)