from django.http import HttpResponse
from django.http import HttpResponseRedirect


###############################################################
###############################################################
###############################################################

def index(request):
    return HttpResponseRedirect("/inventory/room/")
