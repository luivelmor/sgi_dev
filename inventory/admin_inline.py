# django
from django.contrib import admin
# apps
from inventory.forms import DeviceForm, InvoiceForm
from inventory.models import DeviceType, DeviceModel, DeviceModelFile, Invoice, InvoiceFile, DriverFile
from inventory.models import DeviceModelDriverFile, Device, DevicePlace, Tag, MicrophoneFrequency, Room, Place


###############################################################
################# DeviceModelDriverFileInline #################
###############################################################

class DeviceModelDriverFileInline(admin.TabularInline):
    model = DeviceModelDriverFile
    extra = 1

###############################################################
#################### DeviceModelFileInline ####################
###############################################################

class DeviceModelFileInline(admin.TabularInline):
    model = DeviceModelFile
    extra = 2

###############################################################
###################### InvoiceFileInline ######################
###############################################################

class InvoiceFileInline(admin.TabularInline):
    model = InvoiceFile
    extra = 1

###############################################################
######################### DeviceInline ########################
###############################################################

class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0

###############################################################
###################### DevicePlaceInline ######################
###############################################################

class DevicePlaceInline(admin.TabularInline):
    model = DevicePlace

###############################################################
######################## InvoiceInline ########################
###############################################################

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 1