from scripts import Scripts
import requests
import random
import logging
import re

logger = logging.getLogger("notifyme")

class IPChanged(Scripts):
    services = ["http://ifconfig.me/", "http://icanhazip.com/", "http://ident.me/", "http://whatismyip.akamai.com/"]


    def __init__(self, **kwargs):
        #pass remaining arguments to the parent class
        super(IPChanged, self).__init__(**kwargs)

    def __str__(self):
        return "IPChange detector"

    def get_ip(self):
        random.shuffle(self.services)
        for url in self.services:
            try:
                req = requests.get(url, timeout=10)
            except:
                continue

            if req.status_code == 200 and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", req.text.strip()):
                return req.text.strip()

    def do_test(self):
        ip = self.get_ip()
        if ip:
            with open("/var/tmp/ip", "a+") as f:
                ip_from_file = f.readline()
                logger.info(ip + " " + ip_from_file.strip())
                if ip.strip() != ip_from_file.strip():
                    logger.debug("Sending new IP update!")
                    f.truncate(0)
                    f.write(ip)
                    self.notify("New IP: " + ip)
                else:
                    logger.info("No new ip address detected")
