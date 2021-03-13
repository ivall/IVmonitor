import requests
import json

from django.contrib import messages

from config import RECAPTCHA_SECRET_KEY


def verify_captcha(request):
    captcha = request.POST.get("g-recaptcha-response")

    if not captcha:
        return False

    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                      params={'secret': RECAPTCHA_SECRET_KEY, 'response': captcha}).json()

    if not r['success']:
        return False
    return True


def invalid_form(request, form):
    errors = json.loads(form.errors.as_json())

    for error in errors:
        messages.add_message(request, messages.ERROR, message=errors[error][0]['message'])
