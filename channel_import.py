
#Maybe we can dynamically load the channel classes dynamically as well?
from channels.pushover import Pushover
from channels.logfile import LogFile

import ConfigParser
import logging
import os

logger = logging.getLogger("notifyme")

class ChannelImporter(object):

    filename = os.path.dirname(os.path.abspath(__file__)) + "/conf/channels.ini"
    Config = ConfigParser.ConfigParser()

    def __init__(self):
        if not os.path.isfile(self.filename):
            logger.critical("Error loading %s" % (self.filename))

        self.Config.read(self.filename)
        if not self.Config.sections():
            logger.critical("Empty configuration")

        #   Dynamically call the load function for a section:
        #       Every section calls: load_<section name>
        #       where the section name is in lowercase.

        for section in self.Config.sections():
            method_name = "load_" + section.lower()

            if hasattr(self, method_name):
                method = getattr(self, method_name)
                method()
            else:
                logger.critical("The method \"%s\" does not exist in the ChannelImporter class" % (method_name))

    def load_logfile(self):
        LogFile()

    def load_pushover(self):
        if "pushover" not in self.Config.sections():
            logger.critical("[pushover] not specifed")
        else:
            api_token = self.Config.get("pushover", "api_token")
            user_token = self.Config.get("pushover", "user_token")
            Pushover(api_token, user_token)
