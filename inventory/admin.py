# django
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.core import serializers
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars
from django.contrib.admin import ModelAdmin, SimpleListFilter
# apps
from inventory.forms import DeviceForm, InvoiceForm
from inventory.models import DeviceType, DeviceModel, DeviceModelFile, Invoice, InvoiceFile, DriverFile
from inventory.models import DeviceModelDriverFile, Device, DevicePlace, Tag, MicrophoneFrequency, Room, Place
from inventory.admin_actions import *
from inventory.admin_filters import *
from inventory.admin_functions import *
from inventory.admin_inline import *
# libraries
import json
import datetime


###################################################################################################################
#################################################### UserAdmin ####################################################
###################################################################################################################

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'get_groups',
                    'get_last_login')  # don't forget the commas

    def get_last_login(self, obj):
        if obj.last_login is None:
            return "-"
        return obj.last_login.strftime("%d/%m/%Y")

    def get_groups(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    get_groups.short_description = 'Rol'
    get_last_login.short_description = 'Último login'  # Sets column name


#############################################################################################################
############################################## DeviceModelAdmin #############################################
#############################################################################################################

class DeviceModelAdmin(admin.ModelAdmin):
    fields = ('deviceType', 'name', 'alias', 'image', 'image_thumbnail', 'notes')  # fields in form
    list_display = (
        'id', 'get_deviceTypeName', 'get_deviceModelName', 'image_thumbnail', 'get_deviceModelFiles',
        'device_count', 'get_notes')  # fields in instances table
    list_display_links = ('id', 'get_deviceModelName')  # linked fields
    readonly_fields = ('id', 'image_thumbnail',)  # not mapped fields
    list_filter = (('deviceType', customTitledFilter('tipo de dispositivo')),
                   ('name', customTitledFilter('modelo')))  # filtering
    search_fields = ('deviceType__name', 'name', 'devicemodelfile__filename')  # search
    inlines = [
        DeviceModelFileInline
    ]
    ordering = ['-id']

    def device_count(self, obj):
        # http://10.1.21.24/inventory/device/?deviceModel__name=ASRock+-+G31M-GS+-+Intel%28R%29+Core%28TM%292+Duo+CPU+++++E6550++%40+2.33GHz
        count_string = ""
        count_string += '<a href="/inventory/device/?deviceModel__name={}">{}</a><br>'.format(obj.name,
                                                                                              obj.device_count)
        return mark_safe(count_string)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(device_count=Count('device'))

        return queryset

    def get_deviceModelFiles(self, obj):
        files_string = ""
        deviceModelFiles = obj.devicemodelfile_set.all()
        for item in deviceModelFiles.iterator():
            files_string += '<a href="{}{}">{}</a><br>'.format(
                settings.MEDIA_URL,
                item.file, item.filename)
        return mark_safe(files_string)

    get_deviceModelFiles.short_description = 'Model files'

    def get_deviceModelName(self, obj):
        if not obj.alias:
            return obj.name
        return obj.alias

    def get_deviceTypeName(self, obj):
        return obj.deviceType.name

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe('<a href="{}"><img src="{}" width="{}"/></a>'.format(obj.image.url, obj.image.url,
                                                                                  settings.IMAGES_THUMBNAIL_SIZE))
        else:
            return 'No_image_thumbnail'

    def get_notes(self, obj):
        return mark_safe(truncatechars(obj.notes, 500))

    # Renames column head
    get_deviceTypeName.short_description = 'Tipo de dispositivo'
    get_deviceModelName.short_description = 'Modelo'
    image_thumbnail.short_description = 'Imagen'
    get_deviceModelFiles.short_description = 'Archivos'
    device_count.short_description = 'Nº dispositivos'
    get_notes.short_description = 'Notas'
    # Allows column order sorting
    get_deviceTypeName.admin_order_field = 'deviceType__name'
    get_deviceModelName.admin_order_field = 'name'
    device_count.admin_order_field = 'device_count'
    get_notes.admin_order_field = 'notes'


#############################################################################################################
########################################### DeviceModelFilesAdmin ###########################################
#############################################################################################################

class DeviceModelFilesAdmin(admin.ModelAdmin):
    fields = ('deviceModel', 'filename', 'file')  # fields in form
    list_display = (
        'id', 'get_deviceModelTypeName', 'get_deviceModelName', 'filename', 'file')  # fields in instances table
    list_display_links = ('id', 'get_deviceModelName')  # linked fields
    readonly_fields = ('id',)  # not mapped fields
    list_filter = ('deviceModel__name',)  # filtering
    search_fields = ('id', 'deviceModel__name', 'filename', 'file')  # search

    def get_deviceModelTypeName(self, obj):
        return obj.deviceModel.deviceType.name

    def get_deviceModelName(self, obj):
        if not obj.alias:
            return obj.name
        return obj.alias


#########################################################################################################
############################################## InvoiceAdmin #############################################
#########################################################################################################

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    fields = ('reference', 'warranty_from', 'warranty_to', 'notes', 'devices')  # fields in form
    list_display = (
        'id', 'get_reference', 'get_warranty_from', 'get_warranty_to', 'get_invoiceFiles', 'get_invoiceDevices',
        'get_notes', 'get_warranty_status')  # fields in instances table
    list_display_links = ('id', 'get_reference')  # linked fields
    # Error al colocar más de 1 custom filter:
    # Otros filtros posibles: GetInvoiceDeviceModelFilter, GetInvoiceRoomFilter, GetWarrantyStatusFilter,
    list_filter = (GetInvoiceDeviceTypeFilter,)
    inlines = [
        InvoiceFileInline,
    ]
    # Para cambiar de filtro horizontal | vertical a checkbox -> debemos editar InvoiceForm
    filter_vertical = ('devices',)

    def get_reference(self, obj):
        return obj.reference

    def get_warranty_from(self, obj):
        return obj.warranty_from

    def get_warranty_to(self, obj):
        return obj.warranty_to

    def get_warranty_status(self, obj):
        if (datetime.date.today() > obj.warranty_from) & (datetime.date.today() < obj.warranty_to):
            return mark_safe("<span style=\"color:green\">En garantía</span>")
        return mark_safe("<span style=\"color:red\">Sin garantía</span>")

    def get_invoiceFiles(self, obj):
        files_string = ""
        invoiceFiles = obj.invoicefile_set.all()
        for item in invoiceFiles.iterator():
            files_string += '<a href="{}{}">{}</a><br>'.format(
                settings.MEDIA_URL,
                item.file, item.filename)
        return mark_safe(files_string)

    get_invoiceFiles.short_description = 'Archivos'

    def get_notes(self, obj):
        return mark_safe(truncatechars(obj.notes, 500))

    def get_invoiceDevices(self, obj):
        files_string = ""
        invoiceModels = []
        invoiceDevices = []

        for device in obj.devices.all():
            deviceModel = device.deviceModel
            deviceType = device.deviceModel.deviceType.name
            # Guardamos el dispositivo modelo en la lista de dispositivos de la factura
            invoiceDevices.append(device)
            # Guardamos el modelo en la lista de modelos de la factura (si no esta ya incluido)
            if deviceModel not in invoiceModels:
                invoiceModels.append(deviceModel)

        # Iteramos Modelos
        # invoiceModels: obtenemos el alias si existe para acortar los textos de la tabla
        for invoiceModel in invoiceModels:
            deviceModelName = ""
            if not invoiceModel.alias:
                deviceModelName = invoiceModel.name
            else:
                deviceModelName = invoiceModel.alias
            files_string += "<u><strong>" + '<a href="/inventory/devicemodel/{}">{}-{}</a><br>'.format(invoiceModel.id,
                                                                                                       invoiceModel.deviceType.name,
                                                                                                       deviceModelName) + "</strong></u>"

            if invoiceModel.deviceType.name != "Placa base":
                # Iteramos dispositivos
                for invoiceDevice in invoiceDevices:
                    # Mostramos los dispositivos que pertenecezan al modelo iterado
                    if invoiceDevice.deviceModel.name == invoiceModel.name:
                        # DevicePlace info
                        queryset2 = DevicePlace.objects.all().filter(device_id=invoiceDevice.id)
                        if queryset2:
                            for devicePlace in queryset2:
                                files_string += str(devicePlace.place.name)
                        else:
                            files_string += invoiceDevice.room.name
                        # Device ID info
                        files_string += " - ID:" + '<a href="/inventory/device/{}">{}</a>'.format(invoiceDevice.id, invoiceDevice.id)
                        # SerialNumber info
                        if invoiceDevice.serialNumber is not None:
                            files_string += " - Serial:" + invoiceDevice.serialNumber
                        files_string += ", "
                files_string += "<br>"
            files_string += "<br>"

        return mark_safe(files_string)

    get_invoiceFiles.short_description = 'Archivos'

    # Renames column head
    get_reference.short_description = 'Referencia'
    get_warranty_from.short_description = 'Desde'
    get_warranty_to.short_description = 'Hasta'
    get_invoiceDevices.short_description = 'Dispositivos'
    get_notes.short_description = 'Notas'
    get_warranty_status.short_description = "Estado"
    # Allows column order sorting
    get_reference.admin_order_field = 'reference'
    get_warranty_from.admin_order_field = 'warranty_from'
    get_warranty_to.admin_order_field = 'warranty_to'
    get_notes.admin_order_field = 'notes'


###################################################################################################
######################################## InvoiceFilesAdmin ########################################
###################################################################################################

class InvoiceFilesAdmin(admin.ModelAdmin):
    fields = ('invoice', 'filename', 'file')  # fields in form
    list_display = (
        'id', 'get_deviceModelName', 'filename', 'file')  # fields in instances table

    def get_deviceModelName(self, obj):
        return obj.device.deviceModel.name


#######################################################################################################
########################################### DriverFileAdmin ###########################################
#######################################################################################################

class DriverFileAdmin(admin.ModelAdmin):
    fields = ('filename', 'file')  # fields in form
    list_display = ('filename', 'file', 'get_deviceModel')  # fields in instances table
    list_display_links = ('filename',)  # linked fields
    search_fields = ('filename', 'file')  # search
    inlines = [
        DeviceModelDriverFileInline
    ]

    def get_deviceModel(self, obj):
        files_string = ""
        deviceModels = obj.devicemodeldriverfile_set.all()
        for item in deviceModels.iterator():
            files_string += item.deviceModel.deviceType.name + " - " + '<a href="/inventory/devicemodel/{}/change/">{}</a><br>'.format(
                item.deviceModel.pk,
                item.deviceModel.name)
        return mark_safe(files_string)

    # Renames column head
    get_deviceModel.short_description = 'Modelos asociados'


#######################################################################################################
################################################# Store ###############################################
#######################################################################################################

class Store(DeviceModel):
    class Meta:
        proxy = True
        verbose_name = _('Store')
        verbose_name_plural = _('Store')


#######################################################################################################
############################################## StoreAdmin #############################################
#######################################################################################################

class StoreAdmin(DeviceModelAdmin):
    fields = ('deviceType', 'name', 'image', 'image_thumbnail')  # fields in form
    list_display = (
        'get_deviceTypeName', 'get_deviceModelName', 'image_thumbnail', 'get_deviceModelFiles',
        'device_store_count')  # fields in instances table
    list_display_links = ('get_deviceModelName',)  # linked fields
    readonly_fields = ('image_thumbnail',)  # not mapped fields
    list_filter = (('deviceType', customTitledFilter('tipo de dispositivo')),
                   ('name', customTitledFilter('modelo')))  # filtering
    search_fields = ('deviceType__name', 'name', 'devicemodelfile__filename')  # search
    inlines = [
        DeviceModelFileInline
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def device_store_count(self, obj):
        queryset = Device.objects.all().filter(room_id=1, deviceModel__name=obj.name)
        count_string = ""
        if queryset:
            count_string += '<a href="/inventory/device/?deviceModel__name={}&room__name=Almac%C3%A9n">{}</a><br>'.format(
            obj.name, queryset.count())
        return mark_safe(count_string)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(device_count=Count('device')).filter(device__room=1)

        return queryset

    def get_deviceModelFiles(self, obj):
        files_string = ""
        deviceModelFiles = obj.devicemodelfile_set.all()
        for item in deviceModelFiles.iterator():
            files_string += '<a href="{}{}">{}</a><br>'.format(
                settings.MEDIA_URL,
                item.file, item.filename)
        return mark_safe(files_string)

    get_deviceModelFiles.short_description = 'Model files'

    def get_deviceModelName(self, obj):
        if not obj.alias:
            return obj.name
        return obj.alias

    def get_deviceTypeName(self, obj):
        return obj.deviceType.name

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe('<a href="{}"><img src="{}" width="{}"/></a>'.format(obj.image.url, obj.image.url,
                                                                                  settings.IMAGES_THUMBNAIL_SIZE))
        else:
            return 'No_image_thumbnail'

    # Renames column head
    get_deviceTypeName.short_description = 'Tipo de dispositivo'
    get_deviceModelName.short_description = 'Modelo'
    image_thumbnail.short_description = 'Imagen'
    get_deviceModelFiles.short_description = 'Archivos'
    device_store_count.short_description = 'Cantidad'
    # Allows column order sorting
    get_deviceTypeName.admin_order_field = 'deviceType__name'
    get_deviceModelName.admin_order_field = 'name'
    device_store_count.admin_order_field = 'device_count'


###################################################################################################################
#################################################### RoomAdmin ####################################################
###################################################################################################################

class RoomAdmin(admin.ModelAdmin):
    fields = ('name', 'floor')  # fields in form
    list_display = ('get_name', get_devices_from_type('Micrófono'), get_devices_from_type('Proyector'),
                    get_devices_from_type('Amplificador'),
                    get_devices_from_type('Ordenador'))  # fields in instances table
    list_display_links = ('get_name',)  # linked fields
    list_filter = (
        GetRoomWarrantyStatusFilter, 'floor', ('device__deviceModel__name', customTitledFilter('modelo')))  # filtering
    search_fields = ('name', 'floor', 'device__deviceModel__name', 'device__deviceModel__deviceType__name')  # search
    inlines = [
        DeviceInline
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_name(self, obj):
        count_string = ""
        count_string += '<a href="/inventory/device/?room__name={}">{}</a><br>'.format(obj.name, obj.name)
        return mark_safe(count_string)

    # Renames column head
    get_name.short_description = 'Espacio'
    # Columns order
    get_name.admin_order_field = 'floor'


###################################################################################################################
#################################################### PlaceAdmin ###################################################
###################################################################################################################

class PlaceAdmin(admin.ModelAdmin):
    fields = ('room', 'name')  # fields in form
    list_display = ('get_roomName', 'get_name')  # fields in instances table
    list_display_links = ('get_name',)  # linked fields
    list_filter = ('room',)  # filtering
    search_fields = ('room__name', 'name')  # search
    ordering = ['name']

    def get_roomName(self, obj):
        return obj.room.name

    def get_name(self, obj):
        return obj.name

    # Renames column head
    get_roomName.short_description = 'Espacio'
    get_name.short_description = 'Puesto'
    # Columns order
    get_roomName.admin_order_field = 'room__name'
    get_name.admin_order_field = 'name'


###################################################################################################################
################################################# DevicePlaceAdmin ################################################
###################################################################################################################

class DevicePlaceAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ['place__name']
        verbose_name = _('DevicePlace')
        verbose_name_plural = _('DevicesPlaces')


###################################################################################################################
#################################################### TagAdmin #####################################################
###################################################################################################################

class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'color')  # fields in form
    list_display = ('name', 'color')  # fields in instances table
    list_display_links = ('name',)  # linked fields

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


#################################################################################################################
################################################## DeviceAdmin ##################################################
#################################################################################################################

class DeviceAdmin(admin.ModelAdmin):
    form = DeviceForm
    fields = ('room', 'deviceModel', 'image_thumbnail', 'serialNumber', 'notes', 'quantity')  # fields in form
    list_display = ('id', 'get_roomName', 'get_placeName', 'get_deviceTypeName', get_model_link(),
                    'image_thumbnail', 'get_notes', 'get_serial_and_warranty_status')  # fields in instances table
    readonly_fields = ('image_thumbnail',)  # not mapped fields
    list_filter = (GetDeviceWarrantyStatusFilter,
                   ('deviceModel__deviceType__name', customTitledFilter('tipo de dispositivo')),
                   ('room__name', customTitledFilter('Espacio')),
                   ('deviceModel__name', customTitledFilter('Modelo')),
                   ('room__floor', customTitledFilter('Planta')),)  # filtering
    search_fields = (
        'deviceModel__deviceType__name', 'deviceModel__name', 'room__floor', 'room__name',
        'deviceplace__place__name')  # search
    ordering = ['-id']
    inlines = [
        DevicePlaceInline,
    ]
    actions = [move_device_to_store, ]

    def get_roomName(self, obj):
        return obj.room.name

    def get_placeName(self, obj):
        place_name = "-"
        queryset = DevicePlace.objects.all().filter(device_id=obj.id)
        if queryset:
            for devicePlace in queryset:
                place_name = devicePlace.place.name
        return place_name

    def get_roomFloor(self, obj):
        return obj.room.floor

    def get_deviceTypeName(self, obj):
        return obj.deviceModel.deviceType.name

    def get_deviceModelName(self, obj):
        if not obj.alias:
            return obj.name
        return obj.alias

    def get_notes(self, obj):
        return mark_safe(truncatechars(obj.notes, 500))

    def get_serial_and_warranty_status(self, obj):
        string = ""
        queryset = obj.invoice_set.all()
        if queryset:
            for invoice in queryset:
                if (datetime.date.today() > invoice.warranty_from) & (datetime.date.today() < invoice.warranty_to):
                    string = "<span style=\"color:green\">En garantía con la factura: </span>"
                    string += '<a href="/inventory/invoice/{}">{}</a><br>'.format(invoice.id,
                                                                                  invoice.reference)
                else:
                    string = "<span style=\"color:red\">Sin garantía</span><br>"
        else:
            string = "<span style=\"color:red\">Sin garantía</span><br>"

        if obj.serialNumber is not None:
            string += "<br>Serial:{}".format(obj.serialNumber)
        else:
            string += "<br>Serial no anotado"

        return mark_safe(string)

    def image_thumbnail(self, obj):
        if obj.deviceModel.image:
            return mark_safe('<a href="{}"><img src="{}" width="{}"/></a>'.format(obj.deviceModel.image.url,
                                                                                  obj.deviceModel.image.url,
                                                                                  settings.IMAGES_THUMBNAIL_SIZE))
        else:
            return 'No_image_thumbnail'

    # Renames column head
    get_deviceTypeName.short_description = 'Tipo de dispositivo'
    get_deviceModelName.short_description = 'Modelo'
    image_thumbnail.short_description = 'Thumbnail'
    get_roomName.short_description = 'Espacio'
    get_placeName.short_description = 'Puesto'
    get_roomFloor.short_description = 'Planta'
    get_notes.short_description = 'Notas'
    get_serial_and_warranty_status.short_description = 'Serial y garantía'
    move_device_to_store.short_description = 'Mover dispositivo/s al almacén y eliminar la asociación al puesto'
    # column order sorting
    get_roomName.admin_order_field = 'room__name'
    get_deviceTypeName.admin_order_field = 'deviceModel__deviceType__name'  # this field owns to deviceModel attribute from Device model
    get_placeName.admin_order_field = 'deviceplace__place__name'
    get_notes.admin_order_field = 'notes'


#####################################################################################################
###################################### MicrophoneFrequencyAdmin #####################################
#####################################################################################################

class MicrophoneFrequencyAdmin(admin.ModelAdmin):
    fields = ('room', 'frequency', 'channel')  # fields in form
    list_display = ('get_room', 'frequency', 'channel', 'get_roomMicrophone')  # fields in instances table
    list_display_links = ('frequency', 'channel')  # linked fields

    def get_roomMicrophone(self, obj):
        files_string = ""
        queryset = Room.objects.all().filter(name=obj.room.name)
        room_id = queryset[0].pk
        queryset2 = Device.objects.all().filter(room_id=room_id)
        if queryset2:
            for item in queryset2:
                if (item.deviceModel.deviceType.name == "Micrófono"):
                    files_string += '<a href="/inventory/device/{}/change">{}</a><br>'.format(item.id,
                                                                                              item.deviceModel.name)

        return mark_safe(files_string)

    def get_room(self, obj):
        string = ""
        string += '<a href="/inventory/device/?room__name={}">{}</a><br>'.format(obj.room.name, obj.room.name)
        return mark_safe(string)

    # Renames column head
    get_room.short_description = 'Espacio'
    get_roomMicrophone.short_description = 'Micrófono'



#####################################################################################################
############################################## Register #############################################
#####################################################################################################

# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(DeviceType)
admin.site.register(DeviceModel, DeviceModelAdmin)
admin.site.register(DeviceModelFile, DeviceModelFilesAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceFile, InvoiceFilesAdmin)
admin.site.register(DriverFile, DriverFileAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MicrophoneFrequency, MicrophoneFrequencyAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(DevicePlace, DevicePlaceAdmin)
admin.site.register(Store, StoreAdmin)