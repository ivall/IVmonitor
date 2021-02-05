from django.contrib import admin

from .models import MonitorObject, Log, Alert

admin.site.register(MonitorObject)
admin.site.register(Log)
admin.site.register(Alert)
