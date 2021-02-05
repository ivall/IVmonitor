from django.contrib import admin

from .models import MonitorObject, Log

admin.site.register(MonitorObject)
admin.site.register(Log)
