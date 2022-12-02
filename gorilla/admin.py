# django
from django.contrib import admin
from django import forms
from django.conf import settings
from django.db.models import OuterRef, Subquery
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.db.models import Count
# apps
from gorilla.models import Manifest, Event, EventLog, ToolWizStatus, ScreenResolution, ProxyDeviceModelDriverFile, Report
from inventory.models import Place, DevicePlace, Device
from gorilla.admin_filters import *
from gorilla.admin_actions import *
# libraries
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
import datetime
import json
import re


###############################################################
######################## ManifestAdmin ########################
###############################################################

class ManifestAdmin(admin.ModelAdmin):
    fields = ('ip', 'place', 'name')  # fields in form
    list_display = ('get_room_name', 'get_place_name', 'ip', 'name', 'get_last_connection')  # fields in instances table
    list_display_links = ('name',)  # linked fields
    search_fields = ('ip', 'name', 'place__room__name', 'place__name')  # search
    list_filter = ('place__room__name',)  # filtering
    ordering = ['name']
    actions = [reset_last_connection_selected_items, ]

    def get_room_name(self, obj):
        return obj.place.room.name

    def get_place_name(self, obj):
        return obj.place.name

    def get_last_connection(self, obj):
        return obj.last_connection

    # Renames column head
    get_room_name.short_description = 'Espacio'
    get_place_name.short_description = 'Puesto'
    get_last_connection.short_description = 'Última conexión'
    reset_last_connection_selected_items.short_description = 'Resetear fecha de última conexión'
    # Columns order
    get_room_name.admin_order_field = 'place__room__name'
    get_place_name.admin_order_field = 'place__name'
    get_last_connection.admin_order_field = '-last_connection'


###############################################################
########################## EventAdmin #########################
###############################################################

class EventAdmin(admin.ModelAdmin):
    fields = ('eventId', 'description')  # fields in form
    list_display = ('eventId', 'description')  # fields in instances table
    ordering = ['eventId']


###############################################################
######################### EventLogAdmin #######################
###############################################################

class EventLogAdmin(admin.ModelAdmin):
    fields = ('manifest', 'event', 'entryType', 'timeWritten')  # fields in form
    list_display = ('manifest', 'get_ip', 'get_events')  # fields in instances table
    search_fields = ('manifest__name', 'event__eventId', 'entryType', 'timeWritten', 'details')  # search
    list_filter = ('event__eventId', 'manifest__name',)  # filtering
    ordering = ['-timeWritten']
    actions = [delete_all_events_from_manifest, delete_all_events_from_database]

    def get_queryset(self, request):
        return EventLog.objects.filter(
            pk__in=Subquery(
                EventLog.objects.all().distinct('manifest').values('pk')
            )
        ).order_by('manifest')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_ip(self, obj):
        if obj.manifest is not None:
            return obj.manifest.ip
        return "error: no ip"

    def get_events(self, obj):

        def get_event_icon(entryType):
            if entryType == "0":
                return '<i style="color: red" class="fas fa-skull-crossbones"></i> Crítico'
            if entryType == "Error":
                return '<i style="color: red" class="fas fa-exclamation-circle"></i> Error'
            if entryType == "Information":
                return '<i style="color: blue" class="fas fa-info"></i> Información'

            return '<i style="color: blue" class="fas fa-info"></i> Información'

        def day_translation(day):
            switcher = {
                "Monday": "Lunes",
                "Tuesday": "Martes",
                "Wednesday": "Miércoles",
                "Thursday": "Jueves",
                "Friday": "Viernes",
                "Saturday": "Sábado",
                "Sunday": "Domingo",
            }
            return switcher.get(day, "Invalid day")

        files_string = "<table>"
        header_is_set = False
        # JOIN (Manifest X EventLog)
        queryset = EventLog.objects.all().filter(manifest_id=obj.manifest).order_by('-timeWritten')[:20]
        if queryset:
            for eventLog in queryset:
                if not header_is_set:
                    files_string += '<tr><th>ID</th><th style"width: 10px;">Tipo</th><th>Fecha</th><th>Descripción</th></tr>'
                    header_is_set = True

                files_string += '<tr>'
                files_string += '<td>' + eventLog.event.eventId + '</td>'
                files_string += '<td>' + get_event_icon(eventLog.entryType) + '</td>'
                # timeWritten
                day = day_translation(eventLog.timeWritten.strftime("%A"))
                files_string += '<td>' + day + " - " + eventLog.timeWritten.strftime("%d/%m/%Y - %H:%M") + '</td>'
                details_text = ''
                if eventLog.details is not None:
                    details_text = eventLog.details
                files_string += '<td>' + eventLog.event.description + '. ' + details_text + '</td>'
                files_string += '</tr>'
        files_string += '</table>'

        return mark_safe(files_string)

    # Renames column head
    get_ip.short_description = "Dirección ip"
    get_events.short_description = "Eventos"
    delete_all_events_from_manifest.short_description = 'Borrar todos los eventos del manifest seleccionado/s'
    delete_all_events_from_database.short_description = 'Borrar TODOS los eventos de la base de datos'
    # Columns order
    get_ip.admin_order_field = 'manifest__ip'


###############################################################
####################### ToolWizStatusAdmin ####################
###############################################################

class ToolWizStatusAdmin(admin.ModelAdmin):
    fields = ('manifest', 'status')  # fields in form
    list_display = (
        'get_room_name', 'get_place_name', 'get_ip', 'get_status', 'get_last_connection')  # fields in instances table
    list_display_links = ('get_status',)  # linked fields
    search_fields = ('manifest__place__room__name', 'manifest__place__name', 'manifest__ip', 'status')  # search
    list_filter = ('status', 'manifest__place__room__name')  # filtering
    ordering = ['manifest__place__name']
    actions = [freeze_selected_items, unfreeze_selected_items, reset_last_connection_selected_items]

    def get_room_name(self, obj):
        return obj.manifest.place.room.name

    def get_place_name(self, obj):
        return obj.manifest.place.name

    def get_ip(self, obj):
        return obj.manifest.ip

    def get_status(self, obj):
        if obj.status == "ON":
            # <a href="/gorilla/toolwizstatus/127/change/"><img src="/media/images/botellines_congelados.png" width="50px"></a>

            return mark_safe(
                '<img src="{}" width="{}"/>'.format("/media/images/botellines_congelados.png", "50px"))
            # return mark_safe(' <i style="font-size: 20px" class="far fa-snowflake"></i>')

        return obj.status

    def get_last_connection(self, obj):
        return obj.last_connection

    # Renames column head
    get_room_name.short_description = 'Espacio'
    get_place_name.short_description = 'Puesto'
    get_ip.short_description = "Dirección ip"
    get_status.short_description = 'Estado congelación'
    get_last_connection.short_description = 'Última conexión'
    freeze_selected_items.short_description = 'Congelar items seleccionados'
    unfreeze_selected_items.short_description = 'Descongelar items seleccionados'
    reset_last_connection_selected_items.short_description = 'Resetear fecha de última conexión'
    # Columns order
    get_room_name.admin_order_field = 'manifest__place__room__name'
    get_place_name.admin_order_field = 'manifest__place__name'
    get_ip.admin_order_field = 'manifest__ip'
    get_status.admin_order_field = 'status'
    get_last_connection.admin_order_field = '-last_connection'


###############################################################
##################### ScreenResolutionAdmin ###################
###############################################################

class ScreenResolutionAdmin(admin.ModelAdmin):
    fields = ('manifest', 'x', 'y')  # fields in form
    list_display = ('get_room_name', 'get_place_name', 'get_ip', 'x', 'y')  # fields in instances table
    list_display_links = ('x', 'y')  # linked fields
    search_fields = ('place__room__name', 'place__name', 'manifest__ip', 'x', 'y')  # search

    def get_room_name(self, obj):
        return obj.manifest.place.room.name

    def get_place_name(self, obj):
        return obj.manifest.place.name

    def get_ip(self, obj):
        return obj.manifest.ip

    # Renames column head
    get_room_name.short_description = 'Espacio'
    get_place_name.short_description = 'Puesto'
    get_ip.short_description = "Dirección ip"
    # Columns order
    get_room_name.admin_order_field = 'place__room__name'
    get_place_name.admin_order_field = 'place__name'
    get_ip.admin_order_field = 'manifest__ip'


###############################################################
################ ProxyDeviceModelDriverFileAdmin ##############
###############################################################

class ProxyDeviceModelDriverFileAdmin(admin.ModelAdmin):
    list_display = (
        'get_driverFile', 'get_deviceModel', 'get_devices', 'get_download_driverFile')  # fields in instances table

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_deviceModel(self, obj):
        return mark_safe(
            obj.deviceModel.deviceType.name + " - " + '<a href="/inventory/driverfile/{}/change/">{}</a><br>'.format(
                obj.driverFile.id, obj.deviceModel.name, ))

    def get_driverFile(self, obj):
        return mark_safe('<a href="/inventory/driverfile/{}/change/">{}</a><br>'.format(obj.driverFile.id,
                                                                                        obj.driverFile.filename, ))

    def get_download_driverFile(self, obj):
        return mark_safe(
            '<div><center><a href="/media/{}"><i style="font-size:20px" class="fas fa-download"></i></a></center></div>'.format(
                obj.driverFile.file, ))

    def get_devices(self, obj):
        files_string = "<table>"
        header_is_set = False
        # JOIN (DeviceModelDriverFile__deviceModel X device__deviceModel)
        queryset = Device.objects.all().filter(deviceModel_id=obj.deviceModel)
        if queryset:
            for device in queryset:
                # JOIN (device__room X place__room)
                queryset2 = DevicePlace.objects.all().filter(device_id=device)
                if queryset2:
                    for devicePlace in queryset2:
                        # JOIN (place X manifest__place)
                        queryset3 = Manifest.objects.all().filter(place_id=devicePlace.place)
                        if queryset3:
                            for manifest in queryset3:
                                if not header_is_set:
                                    files_string += "<tr><th>Puesto</th><th>Manifest</th><th>IP</th></tr>"
                                    header_is_set = True

                                files_string += '<tr>'
                                files_string += '<td>' + devicePlace.place.name + '</td>'
                                files_string += '<td>' + manifest.name + '</td>'
                                files_string += '<td>' + manifest.ip + '</td>'
                                files_string += '</tr>'
        files_string += '</table>'
        return mark_safe(files_string)

    # Renames column head
    get_deviceModel.short_description = 'Modelos asociados'
    get_driverFile.short_description = 'Driver'
    get_download_driverFile.short_description = "Descargar driver"
    get_devices.short_description = "Dispositivos asociados"
    # Columns order
    get_deviceModel.admin_order_field = 'deviceModel__name'
    get_driverFile.admin_order_field = 'deviceFile__filename'


###############################################################
########################## ReportAdmin ########################
###############################################################

class ReportAdmin(admin.ModelAdmin):
    fields = ('manifest', 'json')  # fields in form
    list_display = ('get_manifest', 'json_prettified', 'created_at')  # fields in instances table
    search_fields = ('json',)  # search
    list_filter = (ReportScheduledTaskErrorsFilter, 'manifest__place__room__name', 'manifest__name',)  # filtering
    readonly_fields = ('json_prettified',)

    def json_prettified(self, obj):
        # Convert the data to sorted, indented JSON
        response = json.dumps(obj.json, sort_keys=True, indent=2)
        # Truncate the data. Alter as needed
        response = response[:5000]
        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')
        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)
        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        # Safe the output
        return mark_safe(style + response)

    def get_manifest(self, obj):
        if obj.manifest is not None:
            return mark_safe('<a href="/gorilla/manifest/{}/change/">{}</a><br>'.format(obj.manifest.id, obj.manifest.name))
        else:
            return " - "

    # Renames column head
    get_manifest.short_description = 'Manifest'
    json_prettified.short_description = 'Reporte'
    # Columns order
    get_manifest.admin_order_field = 'manifest__name'


###############################################################
########################### Register ##########################
###############################################################

admin.site.register(Manifest, ManifestAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventLog, EventLogAdmin)
# admin.site.register(ToolWizStatus, ToolWizStatusAdmin)
admin.site.register(ScreenResolution, ScreenResolutionAdmin)
admin.site.register(ProxyDeviceModelDriverFile, ProxyDeviceModelDriverFileAdmin)
admin.site.register(Report, ReportAdmin)