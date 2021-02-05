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