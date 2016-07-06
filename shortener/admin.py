from django.contrib import admin

# Register your models here.

from .models import Link, Click

admin.site.register(Link)
admin.site.register(Click)