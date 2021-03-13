from django.db import models
from django.utils import timezone

from apps.users.models import User


class MonitorObject(models.Model):  # this name of model really sucks, I need to change it
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()  # every x minutes check status
    next_check = models.CharField(max_length=32, default='2137')  # timestamp
    type = models.CharField(max_length=12)  # website
    # if website
    url = models.URLField()


class Alert(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=16)  # email or webhook
    # if webhook
    url = models.URLField()
    post_value = models.CharField(max_length=1000)


class Log(models.Model):
    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE)
    status = models.BooleanField()
    status_code = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
