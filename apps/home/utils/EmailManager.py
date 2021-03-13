from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token

from config import DOMAIN


class EmailManager:

    def __init__(self, user = None, form = None, monitor = None):
        """
        Constructor of class

        :param user: Model of User, needed only by send_activate_email method
        :param form: Form instance, needed only by send_activate_email method
        :param monitor: Model of MonitorObject, needed only by send_website_is_down_email method
        """
        self.user = user
        self.form = form
        self.monitor = monitor

    def send_activate_email(self):
        """
        Send email with activation link

        :return: none
        """
        mail_subject = 'Aktywacja konta w IVmonitor.'
        template_name = 'users/email_activate.html'

        data = {
            'user': self.user,
            'domain': DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': account_activation_token.make_token(self.user),
        }

        self.send_email(mail_subject, template_name, data)

    def send_website_is_down_email(self):
        """
        Send email when website that user monitoring is down

        :return: none
        """
        mail_subject = f'Strona {self.monitor.name} nie działa poprawnie.'
        template_name = 'panel/website_error.html'

        data = {
            'monitor_object': self.monitor,
            'domain': DOMAIN
        }

        self.send_email(mail_subject, template_name, data)

    def send_email(self, mail_subject, template_name, data):
        """
        Sends email

        :param mail_subject: Subject of email
        :param template_name: Name of html template to render in email
        :param data: Json array with data that template needs

        :return: none
        """
        message = render_to_string(template_name, data)

        if self.form:
            to_email = self.form.cleaned_data.get('email')
        else:
            to_email = self.monitor.user.email

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()