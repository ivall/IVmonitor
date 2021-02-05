import threading
import time
from datetime import datetime
import requests

from .models import MonitorObject
from .notifications import notify_user, website_is_up

sites_to_check = []


def check_site():
    while True:
        if sites_to_check:
            site = sites_to_check[0]
            sites_to_check.remove(site)
            try:
                r = requests.get(site.url).status_code
                r = int(r)
            except:
                r = 500
            if str(r)[0] == '2' or str(r)[0] == '3':
                website_is_up(site)
            else:
                notify_user(site)
        else:
            time.sleep(0.1)


def get_sites():
    t1 = threading.Thread(target=check_site)
    t1.start()
    t2 = threading.Thread(target=check_site)
    t2.start()
    while True:
        objects = MonitorObject.objects.all()
        for object in objects:
            if object not in sites_to_check:
                ts = time.time()
                current_str_time = str(ts)
                if object.next_check == current_str_time or object.next_check < current_str_time or object.next_check == '2137':
                    sites_to_check.append(object)

                    next_check = ts + (60*object.rate)
                    MonitorObject.objects.filter(id=object.id).update(next_check=next_check)
        print(sites_to_check)
        time.sleep(60)
