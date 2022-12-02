# django
from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.utils.safestring import mark_safe
# apps
from inventory.forms import DeviceForm, InvoiceForm
from inventory.models import DeviceType, DeviceModel, DeviceModelFile, Invoice, InvoiceFile, DriverFile
from inventory.models import DeviceModelDriverFile, Device, Place, DevicePlace, Tag, MicrophoneFrequency, Room
# libraries
import datetime


###########################################################
#################### Filtros InvoiceAdmin #################
###########################################################

class GetInvoiceDeviceTypeFilter(admin.SimpleListFilter):
    title = 'Tipo de dispositivo'
    parameter_name = 'filter_by_device_type'

    def lookups(self, request, model_admin):
        deviceTypes = set([c.name for c in DeviceType.objects.all()])
        return [(c, c) for c in deviceTypes]

    def queryset(self, request, queryset):
        if self.value():
            queryset1 = DeviceType.objects.filter(name=self.value()).first()
            queryset2 = Device.objects.filter(deviceModel__deviceType=queryset1)
            queryset3 = Invoice.objects.filter(devices__in=queryset2)
            return queryset3.distinct()
        else:
            queryset1 = DeviceType.objects.filter(name=self.value()).first()
            queryset2 = Device.objects.filter(deviceModel__deviceType=queryset1)
            queryset3 = Invoice.objects.exclude(devices__in=queryset2)
            return queryset3.distinct()


class GetInvoiceDeviceModelFilter(admin.SimpleListFilter):
    title = 'Modelo de dispositivo'
    parameter_name = 'filter_by_device_model'

    def lookups(self, request, model_admin):
        deviceModels = set([c.name for c in DeviceModel.objects.all()])
        return [(c, c) for c in deviceModels]

    def queryset(self, request, queryset):
        if self.value():
            queryset1 = DeviceModel.objects.filter(name=self.value()).first()
            queryset2 = Device.objects.filter(deviceModel=queryset1)
            queryset3 = Invoice.objects.filter(devices__in=queryset2)
            return queryset3.distinct()
        else:
            queryset1 = DeviceModel.objects.filter(name=self.value()).first()
            queryset2 = Device.objects.filter(deviceModel=queryset1)
            queryset3 = Invoice.objects.exclude(devices__in=queryset2)
            return queryset3.distinct()


class GetWarrantyStatusFilter(admin.SimpleListFilter):
    title = 'Garantía'
    parameter_name = 'filter_by_warranty_status'

    def lookups(self, request, model_admin):
        return (
            ('in_warranty', 'En garantía'),
            ('no_warranty', 'Sin garantía'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'in_warranty':
            return Invoice.objects.filter(warranty_to__gt=datetime.date.today())
        elif value == 'no_warranty':
            return Invoice.objects.exclude(warranty_to__gt=datetime.date.today())


class GetInvoiceRoomFilter(admin.SimpleListFilter):
    title = 'Espacios'
    parameter_name = 'invoice_filter_by_room'

    def lookups(self, request, model_admin):
        rooms = set([c.name for c in Room.objects.all()])
        return [(c, c) for c in rooms]

    def queryset(self, request, queryset):
        if self.value():
            queryset1 = Room.objects.filter(name=self.value()).first()
            queryset2 = Device.objects.filter(room=queryset1)
            queryset3 = Invoice.objects.filter(devices__in=queryset2)
            return queryset3.distinct()
        else:
            queryset1 = Room.objects.filter(name=self.value()).first()
            queryset2 = Device.objects.filter(room=queryset1)
            queryset3 = Invoice.objects.exclude(devices__in=queryset2)
            return queryset3.distinct()


###########################################################
#################### Filtros RoomAdmin ####################
###########################################################

class GetRoomWarrantyStatusFilter(admin.SimpleListFilter):
    title = 'Garantía'
    parameter_name = 'filter_by_warranty_status'

    def lookups(self, request, model_admin):
        return (
            ('in_warranty', 'Con algún dispositivo en garantía'),
            ('no_warranty', 'Sin dispositivos en garantía'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'in_warranty':
            queryset1 = Invoice.objects.filter(warranty_to__gt=datetime.date.today()).values('devices')
            queryset2 = Device.objects.all().filter(id__in=queryset1).values('room')
            queryset3 = Room.objects.filter(id__in=queryset2)
            return queryset3
        elif value == 'no_warranty':
            queryset1 = Invoice.objects.filter(warranty_to__gt=datetime.date.today()).values('devices')
            queryset2 = Device.objects.all().filter(id__in=queryset1).values('room')
            queryset3 = Room.objects.exclude(id__in=queryset2)
            return queryset3


##########################################################
#################### Filtros DeviceAdmin #################
##########################################################

class GetDeviceWarrantyStatusFilter(admin.SimpleListFilter):
    title = 'Garantía'
    parameter_name = 'filter_by_warranty_status'

    def lookups(self, request, model_admin):
        return (
            ('in_warranty', 'En garantía'),
            ('no_warranty', 'Sin garantía'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'in_warranty':
            queryset1 = Invoice.objects.filter(warranty_to__gt=datetime.date.today()).values('devices')
            queryset2 = Device.objects.all().filter(id__in=queryset1)
            return queryset2
        elif value == 'no_warranty':
            queryset1 = Invoice.objects.filter(warranty_to__gt=datetime.date.today()).values('devices')
            queryset2 = Device.objects.all().exclude(id__in=queryset1)
            return queryset2