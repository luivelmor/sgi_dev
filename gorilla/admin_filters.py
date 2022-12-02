# django
from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.utils.safestring import mark_safe
# apps
from inventory.forms import DeviceForm, InvoiceForm
from gorilla.models import Manifest, Event, EventLog, ToolWizStatus, ScreenResolution, ProxyDeviceModelDriverFile, Report
from inventory.models import Place, DevicePlace, Device
# libraries
import datetime
import json
import re


##########################################################
#################### Filtros ReportAdmin #################
##########################################################

class ReportScheduledTaskErrorsFilter(admin.SimpleListFilter):
    title = 'Tareas programadas:'
    parameter_name = 'report_scheduled_task_error'

    def lookups(self, request, model_admin):
        return (
            ('with_errors', 'Con errores'),
            ('without_errors', 'Sin errores'),
        )

    def queryset(self, request, queryset):

        def get_report_errors(find_errors):
            reports = Report.objects.all()
            reports_with_error = []

            for report in reports:
                scheduled_task_dict = report.json["Scheduled tasks"]
                scheduled_task_string = json.dumps(scheduled_task_dict)
                result = re.findall("\"LastTaskResult\": [0-9][0-9]", scheduled_task_string)
                if find_errors:
                    if len(result) > 0:
                        reports_with_error.append(report.pk)
                else:
                    if len(result) == 0:
                        reports_with_error.append(report.pk)

            return reports_with_error

        value = self.value()
        if value == 'with_errors':
            return Report.objects.filter(id__in=get_report_errors(True))

        elif value == 'without_errors':
            return Report.objects.filter(id__in=get_report_errors(False))
