from django.conf import settings
from django.urls import include, path
from inventory import views

urlpatterns = [
    path('', views.index, name='index'), # redirect to /inventory/room/
]