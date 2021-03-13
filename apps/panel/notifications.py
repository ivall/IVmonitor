import requests
import json

from .models import Alert, Log, MonitorObject
from apps.home.utils.EmailManager import EmailManager


def notify_user(site, status_code):
    user_alerts = Alert.objects.filter(user_id=site.user.id)
    monitor_object = MonitorObject.objects.filter(id=site.id)[0]

    try:
        latest_log = Log.objects.filter(monitor_object=monitor_object.id).order_by('-id').values('status')[0]
        latest_status = latest_log['status']
        if not latest_status:
            return
    except IndexError:
        pass

    log = Log(
        monitor_object=monitor_object,
        status=False,
        status_code=status_code
    )
    log.save()

    if user_alerts:
        for alert in user_alerts:
            if alert.type == 'email':
                email_manager = EmailManager(monitor=monitor_object)
                email_manager.send_website_is_down_email()

            elif alert.type == 'webhook':
                post_value = alert.post_value.replace('((NAME))', monitor_object.name)
                post_value = post_value.replace('((URL))', monitor_object.url)
                try:
                    json_data = json.loads(post_value)
                except:
                    return
                r = requests.post(alert.url, json=json_data)


def website_is_up(site, status_code):
    monitor_object = MonitorObject.objects.filter(id=site.id)[0]

    try:
        latest_log = Log.objects.filter(monitor_object=monitor_object.id).order_by('-id').values('status')[0]
        latest_status = latest_log['status']
        if latest_status:
            return
    except IndexError:
        pass

    log = Log(
        monitor_object=monitor_object,
        status=True,
        status_code=status_code
    )
    log.save()
