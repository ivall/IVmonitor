from django.db import models

from apps.users.models import User


class MonitorObject(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()  # every x minutes check status
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
