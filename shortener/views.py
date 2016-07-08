from django.shortcuts import get_object_or_404, render, redirect
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from .models import Link, Click
from ipware.ip import get_ip
from random import randint
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


validateUrl = URLValidator()

def IndexView(request):
    template_name = 'shortener/index.html'

    return render(request, template_name)

def LinkHandler(request, identifier):
    ip = get_ip(request)
    print("Handling redirect")
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
    resp_data = None
    
    try:
        validateUrl(link)
    except ValidationError, e:
        return JsonResponse({
            'msg': 'link_validation_error'  
        })

    if len(identifier) == 0:
        identifier = randomIdentifier()
        
    linkCreate = Link(link=link, identifier=identifier, create_date=timezone.now(), create_ip=ip, extension=extension)
    
    try:
        linkCreate.save()
        msg = 'succesfully_created'
        resp_data = identifier
    except IntegrityError as e:
        msg = 'identifier_exists'
        
    return JsonResponse({
        'msg': msg,
        'data': resp_data,
    })

def randomIdentifier():
    #Link.objects.raw('SELECT * FROM link ORDER BY LENGTH(identifier) DESC')[0]
    #Links.objects.get(identifier=identifier)
    charset = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    charset_length = len(charset)
    rtn = ''
    for i in range(1, 5):
        random_digit = randint(0, charset_length - 1)
        
        rtn = rtn + charset[charset_length - random_digit:charset_length - random_digit + 1]
        
    try:
        Link.objects.get(identifier=rtn)
    except (KeyError, Link.DoesNotExist):
        return rtn
        
    return randomIdentifier()
    
