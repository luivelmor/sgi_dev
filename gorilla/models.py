import os
from inventory.models import Place
from inventory.models import DeviceModel
from inventory.models import DeviceModelFile
from inventory.models import DriverFile
from inventory.models import DeviceModelDriverFile
from django.db import models
from django import forms
from uuid import uuid4
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.db.models import JSONField


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

class Manifest(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=False, verbose_name=_('Place'), null=True)
    name = models.CharField(verbose_name=_('Name'), default='default_manifest', max_length=100, unique=True,
                            blank=False)
    ip = models.CharField(verbose_name=_('IP Address'), default='', max_length=15, unique=True, blank=False)
    last_connection = models.DateTimeField(verbose_name=_('Last connection'), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Manifest')
        verbose_name_plural = _('Manifests')


###############################################################
###############################################################
###############################################################

class ToolWizStatus(models.Model):
    TOOLWIZ_STATUS = [
        ('ON', 'ON'),
        ('OFF', 'OFF')
    ]

    manifest = models.ForeignKey(Manifest, on_delete=models.CASCADE, blank=False, verbose_name=_('Manifest'),
                                 related_name='manifest', null=True)
    status = models.CharField(verbose_name=_('Status'), max_length=100, choices=TOOLWIZ_STATUS, blank=False)
    last_connection = models.DateTimeField(verbose_name=_('Last connection'), null=True)

    def __str__(self):
        return self.manifest.place.name + " - " + self.status

    class Meta:
        verbose_name = _('Congelar/Descongelar')
        verbose_name_plural = _('Congelar/Descongelar')


###############################################################
###############################################################
###############################################################

class Event(models.Model):
    eventId = models.CharField(verbose_name=_('Event ID'), max_length=5, unique=True, blank=False)
    description = models.CharField(verbose_name=_('Description'), max_length=1000, unique=False, blank=False)

    def __str__(self):
        return self.eventId + " - " + self.description

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


###############################################################
###############################################################
###############################################################

class EventLog(models.Model):
    manifest = models.ForeignKey(Manifest, on_delete=models.CASCADE, blank=False, verbose_name=_('Manifest'),
                                 related_name='manifest_event_log', null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, verbose_name=_('Event'),
                              related_name='event', null=True)
    entryType = models.CharField(verbose_name=_('Entry Type'), default='', max_length=50, unique=False, blank=False)
    timeWritten = models.DateTimeField(verbose_name=_('Time Written'), null=True)
    details = RichTextField(verbose_name=_('Details'), default='', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.manifest.place.name + " - " + self.event.eventId + " - " + self.timeWritten.strftime(
            "%d/%m/%Y, %H:%M:%S")

    class Meta:
        unique_together = ('manifest', 'event', 'timeWritten',)
        verbose_name = _('Event Log')
        verbose_name_plural = _('Events Logs')


###############################################################
###############################################################
###############################################################

class ScreenResolution(models.Model):
    manifest = models.ForeignKey(Manifest, on_delete=models.CASCADE, blank=False, verbose_name=_('Manifest'), null=True)
    x = models.CharField(verbose_name=_('X'), default='', max_length=4, unique=False, blank=False)
    y = models.CharField(verbose_name=_('Y'), default='', max_length=4, unique=False, blank=False)

    def __str__(self):
        return self.x + " - " + self.y

    class Meta:
        verbose_name = _('ScreenResolution')
        verbose_name_plural = _('ScreenResolutions')


###############################################################
###############################################################
###############################################################

class ProxyDeviceModelDriverFile(DeviceModelDriverFile):
    class Meta:
        proxy = True
        verbose_name = _('Driver relation')
        verbose_name_plural = _('Drivers relation')


###############################################################
###############################################################
###############################################################

class Report(models.Model):
    manifest = models.ForeignKey(Manifest, on_delete=models.CASCADE, blank=False, verbose_name=_('Manifest'),
                                 related_name='manifest_report', null=True)
    json = JSONField(verbose_name=_('Json'), default=dict, blank=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.manifest.name

    class Meta:
        verbose_name = _('Gorilla Report')
        verbose_name_plural = _('Gorilla Reports')
