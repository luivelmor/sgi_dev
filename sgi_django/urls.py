from sgi_django import views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.shortcuts import redirect
import debug_toolbar


urlpatterns = [
    # inventory app
    path('inventory/', include('inventory.urls')),
    # gorilla app
    path('gorilla/', include('gorilla.urls')),
    # admin: IMPORTANTE, esto debe ir despues de incluir las urls de las APP
    path('', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# add debug toolbar in urlpatterns
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]