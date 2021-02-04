import threading
import time
import requests

from .models import MonitorObject

sites_to_check = []


def check_site():
    while True:
        if sites_to_check:
            site = sites_to_check[0]
            sites_to_check.remove(site)
            r = requests.get(site.url).status_code
            print(site.name)
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
                sites_to_check.append(object)
        print(sites_to_check)
        time.sleep(60)