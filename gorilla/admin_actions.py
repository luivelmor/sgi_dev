# django
from django.contrib import admin
# apps
from gorilla.models import Manifest, Event, EventLog, ToolWizStatus, ScreenResolution, ProxyDeviceModelDriverFile, \
    Report
from inventory.models import Place, DevicePlace, Device


#################################################
############# Actions ManifestAdmin #############
#################################################
def reset_last_connection_selected_items(ManifestAdmin, request, queryset):
    queryset.update(last_connection=None)


#################################################
############# Actions EventLogAdmin #############
#################################################
def delete_all_events_from_manifest(EventLogAdmin, request, queryset):
    for obj in queryset:
        queryset = EventLog.objects.filter(manifest=obj.manifest)
        for event in queryset:
            event.delete()


def delete_all_events_from_database(EventLogAdmin, request, queryset):
    for obj in queryset:
        queryset = EventLog.objects.all()
        for event in queryset:
            event.delete()


###############################################
########## Actions ToolWizStatusAdmin #########
###############################################
def freeze_selected_items(ToolWizStatusAdmin, request, queryset):
    queryset.update(status='ON')


def unfreeze_selected_items(ToolWizStatusAdmin, request, queryset):
    queryset.update(status='OFF')


def reset_last_connection_selected_items(ToolWizStatusAdmin, request, queryset):
    queryset.update(last_connection=None)