from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from gorilla.models import Manifest
from gorilla.models import Event
from gorilla.models import EventLog
from gorilla.models import ToolWizStatus
from gorilla.models import ScreenResolution
from gorilla.models import Report
from inventory.models import DeviceModel
from inventory.models import DevicePlace
from inventory.models import DeviceType
from inventory.models import DeviceModelDriverFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
import json


###############################################################
###############################################################
###############################################################

def get_manifest_from_ip(request, ip):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/get_manifest_from_ip/10.1.21.230" -UseBasicParsing
    # $content.Content

    # get Manifest object
    item = Manifest.objects.filter(ip=ip).first()
    # status value
    if item is None:
        manifest = "default_manifest"
    else:
        manifest = item.name
        item.last_connection = datetime.datetime.now()
        item.save()
    # html
    html = "%s" % (manifest,)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def get_ip_from_manifest(request, manifest):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/get_ip_from_manifest/aulaTeoria21_manifest" -UseBasicParsing
    # $content.Content

    # get Manifest object
    item = Manifest.objects.filter(name=manifest).first()
    # status value
    if item is None:
        ip = "null"
    else:
        ip = item.ip
    # html
    html = "%s" % (ip,)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def get_toolwiz_status_from_manifest(request, manifest):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/get_toolwizstatus_from_manifest/aulaTeoria21_manifest" -UseBasicParsing
    # $content.Content

    # get ToolWizStatus object
    item = ToolWizStatus.objects.filter(manifest__name=manifest).first()
    # status value
    if item is None:
        status = "null"
    else:
        status = item.status
        item.last_connection = datetime.datetime.now()
        item.save()
    # html
    html = "%s" % (status,)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def get_toolwiz_status_from_ip(request, ip):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/get_toolwizstatus_from_ip/10.1.21.230" -UseBasicParsing
    # $content.Content

    # get ToolWizStatus object
    item = ToolWizStatus.objects.filter(manifest__ip=ip).first()
    # status value
    if item is None:
        status = "null"
    else:
        now = datetime.datetime.now()
        ## 24 hour format now.strftime("%H") ##
        ## 12 hour format now.strftime("%I") ##
        hour = now.strftime("%H")

        if (int(hour) < 5) or (int(hour) > 23):
            html = "%s" % ('UPDATE',)
            return HttpResponse(html)

        status = item.status
        item.last_connection = now
        item.save()
    # html
    html = "%s" % (status,)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def get_screen_resolution_from_ip(request, ip):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/get_screen_resolution_from_ip/10.1.21.230" -UseBasicParsing
    # $content.Content

    # get Place object from ip
    item = ScreenResolution.objects.filter(manifest__ip=ip).first()
    # status value
    if item is None:
        screen_resolution = "null"
    else:
        screen_resolution = item.x + "x" + item.y

    # html
    html = "%s" % (screen_resolution,)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def get_drivers_from_ip(request, ip):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/get_drivers_from_ip/10.1.21.230" -UseBasicParsing
    # $content.Content

    html = "null"

    try:
        # get Manifest object
        item = Manifest.objects.filter(ip=ip).first()
        # status value
        if item is None:
            driverFile = "null"
            driverFilename = "null"
            deviceModel = "null"
        else:
            manifest = item.name
            place = item.place
            # get DevicePlace object
            devicePlace = DevicePlace.objects.filter(place_id=place).first()
            deviceModel = devicePlace.device.deviceModel
            # get DeviceModelDriverFile
            deviceModelDriverFile = DeviceModelDriverFile.objects.filter(deviceModel_id=deviceModel).first()
            driverFilename = deviceModelDriverFile.driverFile.filename
            driverFile = settings.MEDIA_URL + str(deviceModelDriverFile.driverFile.file)

            html = "http://10.1.21.24%s,%s,%s" % (driverFile, driverFilename, deviceModel)

    except Exception as e:
        html = "null"

    # html
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def add_event_log(request, ip, eventId, entryType, timestamp):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/add_event_log/X/Y/Z" -UseBasicParsing
    # $content.Content

    # get Manifest object
    manifest = Manifest.objects.filter(ip=ip).first()

    # Convertimos timestamp a datetime
    from datetime import datetime
    import pytz
    local_tz = pytz.timezone("Europe/Madrid")
    utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    timeWritten = local_tz.normalize(utc_dt.astimezone(local_tz))

    # Obtenemos el evento
    event = Event.objects.filter(eventId=eventId).first()

    # Creamos un objeto EventLog con los datos obtenidos mediante URL
    if manifest is not None:
        eventLog = EventLog(manifest=manifest, event=event, entryType=entryType, timeWritten=timeWritten, details=None)
        eventLog.save()

    html = "%s<br>%s<br>%s<br>%s" % (ip, eventId, entryType, timestamp)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def add_shutdown_event_log(request, ip, eventId, entryType, timestamp, shutdown_type):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/add_shutdown_event_log/X/Y/Z/A" -UseBasicParsing
    # $content.Content

    # get Manifest object
    manifest = Manifest.objects.filter(ip=ip).first()

    # Convertimos timestamp a datetime
    from datetime import datetime
    import pytz
    local_tz = pytz.timezone("Europe/Madrid")
    utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    timeWritten = local_tz.normalize(utc_dt.astimezone(local_tz))

    # Obtenemos el evento
    event = Event.objects.filter(eventId=eventId).first()

    # Creamos un objeto EventLog con los datos obtenidos mediante URL
    eventLog = EventLog(manifest=manifest, event=event, entryType=entryType, timeWritten=timeWritten,
                        details=shutdown_type)
    eventLog.save()

    html = "%s<br>%s<br>%s<br>%s<br>%s" % (ip, eventId, entryType, timestamp, shutdown_type)
    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

def set_computer_model(request, ip, cpu, motherboard):
    # $content = Invoke-WebRequest "http://10.1.21.24/gorilla/set_computer_model/X/Y/Z/A" -UseBasicParsing
    # $content.Content

    # get Manifest object
    manifest = Manifest.objects.filter(ip=ip).first()

    # obtenemos el puesto
    place = manifest.place
    devicePlace = DevicePlace.objects.filter(place_id=place).first()

    # modelo
    device = devicePlace.device
    deviceModel = devicePlace.device.deviceModel

    # Comprobamos si existe el modelo y en caso contrario lo creamos
    deviceModel_name = motherboard + " - " + cpu
    deviceModel_found = DeviceModel.objects.filter(name=str(deviceModel_name)).first()
    deviceModel_count = DeviceModel.objects.filter(name=deviceModel_name).count()

    # si NO existe el modelo
    if (deviceModel_count == 0):
        # Crea un nuevo modelo
        deviceType = DeviceType.objects.filter(name="Ordenador").first()
        newDeviceModel = DeviceModel(name=motherboard + " - " + cpu, deviceType=deviceType)
        newDeviceModel.save()
        # Asigna el modelo
        device.deviceModel = newDeviceModel
        device.save()
    # si existe el modelo
    else:
        # Asigna el modelo
        device.deviceModel = deviceModel_found
        device.save()

    html = "%s<br>%s<br>%s<br>%s<br>%s<br>%s" % (
        "IP: " + ip,
        "Manifest: " + manifest.name,
        "Puesto: " + place.name,
        "Placa - CPU: " + motherboard + " - " + cpu,
        deviceModel_found,
        deviceModel_count)

    return HttpResponse(html)


###############################################################
###############################################################
###############################################################

@csrf_exempt
def add_gorilla_report(request, manifest):
    # $uri = "https://10.1.21.24/gorilla/add_gorilla_report/10.1.21.89"
    # $Body = @{
    #     json_data = $data | ConvertTo-Json
    # }
    #
    # Invoke-RestMethod -Method POST -Uri $uri -Body $Body

    current_time = datetime.datetime.now()
    date_time = current_time.strftime("%m/%d/%Y, %H:%M:%S")

    # Manifest object
    manifest_object = Manifest.objects.filter(name=manifest).first()

    # eliminamos todos los report antiguos
    reports_to_delete = Report.objects.filter(manifest=manifest_object)
    reports_to_delete.delete()

    # guardamos un nuevo report
    json_data = request.POST['json_data']
    json_object = json.loads(json_data)
    gorillaReport = Report(manifest=manifest_object, json=json_object)
    gorillaReport.save()

    return HttpResponse(str(type(json_object)))

