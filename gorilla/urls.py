from django.conf import settings
from django.urls import include, path
from gorilla import views

urlpatterns = [
    # manifest
    path('get_manifest_from_ip/<str:ip>', views.get_manifest_from_ip, name='get_manifest_from_ip'),
    path('get_ip_from_manifest/<str:manifest>', views.get_ip_from_manifest, name='get_ip_from_manifest'),
    # toolwiz
    path('get_toolwizstatus_from_manifest/<str:manifest>', views.get_toolwiz_status_from_manifest, name='get_toolwiz_status_from_manifest'),
    path('get_toolwizstatus_from_ip/<str:ip>', views.get_toolwiz_status_from_ip, name='get_toolwiz_status_from_ip'),
    # screen resolution
    path('get_screen_resolution_from_ip/<str:ip>', views.get_screen_resolution_from_ip, name='get_screen_resolution_from_ip'),
    # drivers
    path('get_drivers_from_ip/<str:ip>', views.get_drivers_from_ip, name='get_drivers_from_ip'),
    # events logs
    path('add_event_log/<str:ip>/<str:eventId>/<str:entryType>/<int:timestamp>', views.add_event_log, name='add_event_log'),
    # shutdown event logs
    path('add_shutdown_event_log/<str:ip>/<str:eventId>/<str:entryType>/<int:timestamp>/<str:shutdown_type>', views.add_shutdown_event_log, name='add_shutdown_event_log'),
    # set computer model
    path('set_computer_model/<str:ip>/<str:cpu>/<str:motherboard>', views.set_computer_model, name='set_computer_model'),
    # GorillaReport
    path('add_gorilla_report/<str:manifest>', views.add_gorilla_report, name='add_gorilla_report'),
]