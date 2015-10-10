
#Maybe we can dynamically load the channel classes dynamically as well?
from channels.pushover import Pushover
from channels.logfile import LogFile

import ConfigParser
import logging
import os

class ChannelImporter(object):
    filename = "channels.ini"
    Config = ConfigParser.ConfigParser()

    def __init__(self):
        if not os.path.isfile(self.filename):
            logging.critical("Error loading %s" % (self.filename))

        self.Config.read(self.filename)
        if not self.Config.sections():
            logging.critical("Empty configuration")

        #TODO:  A way nicer way of doing this is looking at the sections
        #       in the ini file, and loading the modules below accordingly.

    def load_logfile(self):
        LogFile()

    def load_pusher(self):
        if "pushover" not in self.Config.sections():
            logging.critical("[pushover] not specifed")
        else:
            api_token = self.Config.get("pushover", "api_token")
            user_token = self.Config.get("pushover", "user_token")
            Pushover(api_token, user_token)
