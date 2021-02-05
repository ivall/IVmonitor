import requests
import json

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config import DOMAIN

from .models import Alert, Log, MonitorObject

def notify_user(site):
    user_alerts = Alert.objects.filter(user_id=site.user.id)
    monitor_object = MonitorObject.objects.filter(id=site.id)[0]

    try:
        latest_log = Log.objects.filter(monitor_object=monitor_object.id).order_by('-id').values('status')[0]
        latest_status = latest_log['status']
        if latest_status == 'down':
            return
    except IndexError:
        pass

    log = Log(
        monitor_object=monitor_object,
        status='down',
    )
    log.save()

    if user_alerts:
        for alert in user_alerts:
            if alert.type == 'email':
                mail_subject = f'Strona {site.name} nie działa poprawnie.'
                message = render_to_string('panel/website_error.html', {
                    'monitor_object': monitor_object,
                    'domain': DOMAIN
                })
                to_email = site.user.email

                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            elif alert.type == 'webhook':
                post_value = alert.post_value.replace('((NAME))', monitor_object.name)
                post_value = post_value.replace('((URL))', monitor_object.url)
                try:
                    json_data = json.loads(post_value)
                except:
                    return
                r = requests.post(alert.url, json=json_data)


def website_is_up(site):
    monitor_object = MonitorObject.objects.filter(id=site.id)[0]

    try:
        latest_log = Log.objects.filter(monitor_object=monitor_object.id).order_by('-id').values('status')[0]
        latest_status = latest_log['status']
        if latest_status == 'up':
            return
    except IndexError:
        pass

    log = Log(
        monitor_object=monitor_object,
        status='up',
    )
    log.save()
