from django.shortcuts import render_to_response
from django.conf import settings

def homepage(request):
    return render_to_response('homepage.html', {'current_date': settings.MEDIA_ROOT})