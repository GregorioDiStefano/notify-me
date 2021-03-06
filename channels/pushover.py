import httplib
import urllib
import logging
from channels import Channel

logger = logging.getLogger("notifyme")

class Pushover(Channel):

    api_token = ""
    user_token = ""

    def __init__(self, api_token, user_token, **kwargs):
        self.api_token = api_token
        self.user_token = user_token
        super(Pushover, self).__init__()

    def __str__(self):
        return "<%s> using api_token: %s and user_token: %s" % (self.channel_name, self.api_token, self.user_token)

    def do_send_msg(self, msg):
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                    urllib.urlencode({"token": self.api_token,
                                    "user": self.user_token,
                                    "message": msg}),
                    {"Content-type": "application/x-www-form-urlencoded"})
        response = conn.getresponse()
        if response.status != 200:
            logger.critical("Pusherover API call did not repsonse with HTTP 200 OK")

