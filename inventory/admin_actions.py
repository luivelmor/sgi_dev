# django
from django.contrib import admin
# apps
from inventory.models import DeviceType, DeviceModel, DeviceModelFile, Invoice, InvoiceFile, DriverFile
from inventory.models import DeviceModelDriverFile, Device, Place, DevicePlace, Tag, MicrophoneFrequency, Room


#################################################
############## Actions DeviceAdmin ##############
#################################################
def move_device_to_store(DeviceAdmin, request, queryset):
    ids = queryset.values_list('pk', flat=True)
    for id in ids:
        device_place = DevicePlace.objects.filter(device_id=id)
        device_place.delete()
    queryset.update(room=1)