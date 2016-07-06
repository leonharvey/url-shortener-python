from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone


class Link(models.Model):
    link = models.CharField(max_length=150)
    extension = models.CharField(max_length=3, blank=True)
    identifier = models.CharField(max_length=20, unique=True)
    create_date = models.DateTimeField('date published')
    create_ip = models.CharField(max_length=39)
    
    def __str__(self):
        return self.link
        
class Click(models.Model):
    link_identifier = models.CharField(max_length=20)
    create_date = models.DateTimeField('date published')
    create_ip = models.CharField(max_length=39)
    referrer = models.CharField(max_length=150, blank=True)
    
    def __str__(self):
        return self.create_ip
