from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InventoryConfig(AppConfig):
    name = 'inventory'
    label = 'inventory'
    verbose_name = _('Inventory')
