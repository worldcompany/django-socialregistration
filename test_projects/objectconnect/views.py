from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('index.html', {'socialregistration_connect_object': Site.objects.get(pk=1)}, context_instance=RequestContext(request))

def index2(request):
    return render_to_response('index.html', {'socialregistration_connect_object': Site.objects.get(pk=2)}, context_instance=RequestContext(request))
