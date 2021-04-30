# django config
DJANGO_SECRET_KEY = ''

# recaptcha config
RECAPTCHA_SECRET_KEY = ''

# database config
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# email config
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

# monitor config
MONITOR_TYPES = ['website']
RATE_TIME = range(1,60)  # in minutes
MAX_USER_MONITORS = 10

# alert config
ALERT_TYPES = ['email', 'webhook']

# global config
DOMAIN = ''
