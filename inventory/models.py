import os
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


###############################################################
########################## Functions ##########################
###############################################################

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


###############################################################
###############################################################
###############################################################

class DeviceType(models.Model):
    name = models.CharField(verbose_name=_('Name'), default='', max_length=25, unique=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Device type')
        verbose_name_plural = _('Device types')
        ordering = ('name',)


###############################################################
###############################################################
###############################################################

class DeviceModel(models.Model):
    name = models.CharField(verbose_name=_('Name'), default='', max_length=100, unique=True, blank=False)
    alias = models.CharField(verbose_name=_('Alias'), default='', max_length=100, blank=True)
    deviceType = models.ForeignKey(DeviceType, on_delete=models.CASCADE, blank=False, verbose_name=_('Device type'))
    image = models.ImageField(default='inventory/deviceModel_images/default.png',
                              upload_to=PathAndRename(settings.MODEL_IMAGES_PATH),
                              blank=True, verbose_name=_('Image'))
    notes = RichTextField(verbose_name=_('Notes'), default='', max_length=500, blank=True)

    def __str__(self):
        return self.deviceType.name + " - " + self.name

    class Meta:
        verbose_name = _('Device model')
        verbose_name_plural = _('Device models')
        ordering = ('deviceType', 'name')


###############################################################
###############################################################
###############################################################

class DeviceModelFile(models.Model):
    deviceModel = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, blank=False, verbose_name=_('Device model'))
    filename = models.CharField(default='', max_length=150, blank=False, verbose_name=_('Filename'))
    file = models.FileField(verbose_name=_('File'), upload_to=PathAndRename(settings.MODEL_FILES_PATH), blank=False)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = _('Device model file')
        verbose_name_plural = _('Device model files')


###############################################################
###############################################################
###############################################################

class DriverFile(models.Model):
    filename = models.CharField(default='', max_length=150, blank=False, verbose_name=_('Filename'))
    file = models.FileField(verbose_name=_('File'), upload_to=PathAndRename(settings.DRIVER_FILES_PATH), blank=False)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = _('Driver file')
        verbose_name_plural = _('Drivers files')


###############################################################
###############################################################
###############################################################

class DeviceModelDriverFile(models.Model):
    deviceModel = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, blank=False, verbose_name=_('Device model'))
    driverFile = models.ForeignKey(DriverFile, on_delete=models.CASCADE, blank=False, verbose_name=_('Driver file'))

    def __str__(self):
        return self.deviceModel.name + " - " + self.driverFile.filename

    class Meta:
        verbose_name = _('Device model driver file')
        verbose_name_plural = _('Device models drivers files')


###############################################################
###############################################################
###############################################################

class Room(models.Model):
    FLOOR_VALUES = [
        ('Planta 0', 'Planta 0'),
        ('Planta 1', 'Planta 1'),
        ('Planta 2', 'Planta 2'),
        ('Planta 3', 'Planta 3'),
        ('Planta 4', 'Planta 4'),
    ]
    name = models.CharField(verbose_name=_('Name'), default='', max_length=100, unique=True, blank=False)
    floor = models.CharField(verbose_name=_('Floor'), max_length=100, choices=FLOOR_VALUES, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')


###############################################################
###############################################################
###############################################################

class Device(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, verbose_name=_('Room'), null=True)
    deviceModel = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, blank=False, verbose_name=_('Device model'))
    serialNumber = models.CharField(verbose_name=_('Serial'), max_length=100, blank=True, null=True)
    notes = RichTextField(verbose_name=_('Notes'), default='', max_length=500, blank=True)

    def __str__(self):
        if not self.deviceModel.alias:
            deviceModelName = self.deviceModel.name
        else:
            deviceModelName = self.deviceModel.alias

        return str(self.id) + " - " + \
               self.room.name + " - " + \
               self.deviceModel.deviceType.name + " - " + \
               deviceModelName

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')


###############################################################
###############################################################
###############################################################

class Place(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, verbose_name=_('Room'), null=True)
    name = models.CharField(verbose_name=_('Name'), default='', max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.room.name + " - " + self.name

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ('name',)


###############################################################
###############################################################
###############################################################

class Invoice(models.Model):
    reference = models.CharField(verbose_name=_('Reference'), default='', max_length=100, unique=True, blank=False)
    warranty_from = models.DateField(verbose_name=_('Warranty from'))
    warranty_to = models.DateField(verbose_name=_('Warranty to'))
    notes = RichTextField(verbose_name=_('Notes'), default='', max_length=500, blank=True)
    devices = models.ManyToManyField(Device, blank=True, verbose_name=_('Devices'))

    def __str__(self):
        return self.reference

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


###############################################################
###############################################################
###############################################################

class InvoiceFile(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=False, verbose_name=_('Invoice'))
    filename = models.CharField(default='', max_length=150, blank=False, verbose_name=_('Filename'))
    file = models.FileField(verbose_name=_('File'), upload_to=PathAndRename(settings.INVOICE_FILES_PATH), blank=False)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = _('Invoice file')
        verbose_name_plural = _('Invoice files')


###############################################################
###############################################################
###############################################################

class Tag(models.Model):
    name = models.CharField(verbose_name=_('Tag'), default='', max_length=20, unique=True, blank=False)
    color = models.CharField(verbose_name=_('Color'), default='#b70505', max_length=20, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


###############################################################
###############################################################
###############################################################

class DevicePlace(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, blank=False, verbose_name=_('Place'), null=True)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, blank=False, verbose_name=_('Device'))
    tags = models.ManyToManyField(Tag, blank=True,)

    def __str__(self):
        return self.place.name + " - " + \
               self.device.deviceModel.name

    class Meta:
        verbose_name = _('DevicePlace')
        verbose_name_plural = _('DevicesPlaces')


###############################################################
###############################################################
###############################################################

class MicrophoneFrequency(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, blank=False, verbose_name=_('Room'), unique=True,
                                null=True)
    frequency = models.CharField(verbose_name=_('Frequency'), default='', max_length=100, blank=True)
    channel = models.CharField(verbose_name=_('Channel'), default='', max_length=100, blank=True)

    def __str__(self):
        return self.room.name + " - " + self.frequency + " - " + self.channel

    class Meta:
        verbose_name = _('Microphone frequency')
        verbose_name_plural = _('Microphone frequencies')
        ordering = ('room',)

