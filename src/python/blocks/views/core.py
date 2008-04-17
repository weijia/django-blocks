from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

def homepage(request):
    return render_to_response('homepage.html', {}, RequestContext(request))