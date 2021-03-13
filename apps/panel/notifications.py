import requests
import json

from .models import Alert, Log, MonitorObject
from apps.home.utils.EmailManager import EmailManager


class Notifications:
    def __init__(self, site, status_code):
        """
        Constructor of class

        :param site: MonitorObject model instance
        :param status_code: Status code of website
        """
        self.site = site
        self.status_code = status_code
        self.monitor = MonitorObject.objects.filter(id=site.id)[0]

    def latest_log(self, status: bool):
        """
        Checks latest log for monitoring object

        :param status: current status of website, false if website is down, true if website is up
        :return: bool, true if we want save log, false if we don't want save log
        """
        try:
            latest_log = Log.objects.filter(monitor_object=self.monitor.id).order_by('-id').values('status')[0]
            latest_status = latest_log['status']

            if not status and not latest_status:
                return False # latest status for this website is down, it's not needed to log error
            elif status and latest_status:
                return False # latest status for this website is up, it's not needed to log it

            return True
        except IndexError:
            return True

    def save_log(self, status: bool):
        """
        Saves log

        :param status: current status of website, false if website is down, true if website is up
        :return: false if method latest_log returns false else returns none
        """
        if not self.latest_log(status=status):
            return False  # latest log is same as current log, there is no sense to save it

        log = Log(
            monitor_object=self.monitor,
            status=status,
            status_code=self.status_code
        )
        log.save()

    def website_is_down(self):
        """
        Method called when website is down, notifies user about that

        :return: none
        """
        user_alerts = Alert.objects.filter(user_id=self.site.user.id)

        if not self.save_log(status=False):
            return

        if user_alerts:
            for alert in user_alerts:
                if alert.type == 'email':
                    email_manager = EmailManager(monitor=self.monitor)
                    email_manager.send_website_is_down_email()

                elif alert.type == 'webhook':
                    post_value = alert.post_value.replace('((NAME))', self.monitor.name)
                    post_value = post_value.replace('((URL))', self.monitor.url)
                    try:
                        json_data = json.loads(post_value)
                    except:
                        return
                    requests.post(alert.url, json=json_data)

    def website_is_up(self):
        """
        Method called when website is down

        :return: none
        """
        self.save_log(status=True)
