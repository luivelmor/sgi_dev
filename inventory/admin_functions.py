# django
from django.contrib import admin
from django.utils.safestring import mark_safe
# apps
from inventory.forms import DeviceForm, InvoiceForm
from inventory.models import DeviceType, DeviceModel, DeviceModelFile, Invoice, InvoiceFile, DriverFile
from inventory.models import DeviceModelDriverFile, Device, Place, DevicePlace, Tag, MicrophoneFrequency, Room
# libraries
import datetime


###################################################################################################################
#################################################### Functions ####################################################
###################################################################################################################

def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def get_devices_from_type(type_name):
    def _get_devices_from_type(obj):
        # variables
        data = []
        place = ""
        files_string = ""

        # obtenemos todos los dispositivos de un espacio dado (obj = room)
        devices = Device.objects.filter(room=obj, deviceModel__deviceType__name=type_name)
        for item in devices.iterator():
            # obtenemos el puesto del dispositivo (si lo tiene asignado)
            queryset = DevicePlace.objects.all().filter(device_id=item.id)
            # data
            if queryset:
                for devicePlace in queryset:
                    place = devicePlace.place.name + " - "
                    tags = devicePlace.tags.all()
                    # obtenemos las etiquetas del puesto del dispositivo (si tiene alguna/s asignada/s)
                    if tags is not None:
                        for tag in tags:
                            place += '<span style="color: ' + tag.color + ';"><strong>' + tag.name + "</strong></span> - "
            else:
                place = ""

            # obtenemos la garantía
            warranty_status_color = ""
            queryset1 = Invoice.objects.filter(warranty_to__gt=datetime.date.today()).values('devices')
            queryset2 = Device.objects.all().filter(id__in=queryset1).filter(id=item.id)
            if queryset2:
                for device in queryset2:
                    warranty_status_color = "green"

            # guardamos la información en un array
            data_item = []

            # deviceModel alias || name
            deviceModelName = ""
            if not item.deviceModel.alias:
                deviceModelName = item.deviceModel.name
            else:
                deviceModelName = item.deviceModel.alias

            data_item = {
                'place': place,
                'id': item.id,
                'deviceModel': item.deviceModel,
                'deviceModelName': deviceModelName,
                'warranty_status_color': warranty_status_color
            }
            data.append(data_item)

        # ordenamos la información por el número del puesto
        data_order_by_place = sorted(data, key=lambda k: k['place'])
        for item in data_order_by_place:
            if item['deviceModel'].deviceType.name == type_name:
                files_string += '{}<a href="/inventory/device/{}/change" style="color:{};">{}</a><br>'.format(
                    item['place'], item['id'], item['warranty_status_color'], item['deviceModelName'])

        return mark_safe(files_string)

    if type_name == 'Ordenador':
        _get_devices_from_type.short_description = "Puesto/Ordenador"  # Sets column name
    else:
        _get_devices_from_type.short_description = type_name  # Sets column name

    return _get_devices_from_type


def get_model_link():
    def _get_model_link(obj):
        files_string = ""
        model = obj.deviceModel
        files_string += '<a href="/inventory/devicemodel/{}/change">{}</a><br>'.format(model.id,
                                                                                       model.name)
        return mark_safe(files_string)

    _get_model_link.short_description = 'Modelo'  # Sets column name
    _get_model_link.admin_order_field = 'deviceModel__name'  # Column order

    return _get_model_link