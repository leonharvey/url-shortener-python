from django.shortcuts import get_object_or_404, render, redirect
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from .models import Link, Click
from ipware.ip import get_ip
import json
import validators

def IndexView(request):
    template_name = 'shortener/index.html'

    return render(request, template_name)

def LinkHandler(request, identifier):
    ip = get_ip(request)

    referrer = request.META['HTTP_REFERER'] if request.META.get('HTTP_REFERER') else ''

    linkResult    = get_object_or_404(Link, identifier=identifier)

    clickAnalytic = Click(link_identifier=linkResult.identifier, create_date=timezone.now(), create_ip=ip, referrer=referrer)
    clickAnalytic.save()
    
    return redirect(linkResult.link)
    
def AddLink(request):
    extension = request.POST['extension'] if request.POST.get('extension') else ''
    link = request.POST.get('link')
    identifier = request.POST.get('identifier')
    ip = get_ip(request)

    if not validators.url(link):
        return HttpResponse(json.dumps({
            'msg': 'link_validation_error'  
        }))

    linkCreate = Link(link=link, identifier=identifier, create_date=timezone.now(), create_ip=ip, extension=extension)
    
    try:
        linkCreate.save()
        msg = 'succesfully_created'
    except IntegrityError as e:
        msg = 'identifier_exists'
        
    return HttpResponse(json.dumps({
        'msg': msg  
    }))

def rand(length):
    charset = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    