from abc import ABCMeta, abstractmethod
import time
import re
import logging
import sys
from datetime import datetime

sys.path.append("..")
from channels.channels import Channel
logger = logging.getLogger("notifyme")

class Scripts(object):
    __metaclass__ = ABCMeta
    title = ""
    description = ""
    retries = 4
    runtime = "5s"
    send_notification = False
    debug = False
    subscribed_channels = set()

    last_run_time = int(time.time())

    def __init__(self, **kwargs):
        self.subscribed_channels = set()

        if "runtime" in kwargs:
            self.runtime = kwargs["runtime"]
        if "debug" in kwargs:
            self.debug = kwargs["debug"]
        if "channel" in kwargs:
            self.subscribe_channel(kwargs["channel"])
        else:
            logger.critical("no communication channel for %s", self)
        if "send_notification" in kwargs:
            self.send_notification = kwargs["send_notification"]

        #TODO: check if config enters invalid key

    def __str__(self):
        str_format = "<%s>" % (self.title)
        return str_format

    @abstractmethod
    def do_test(self):
        pass

    def do(self):
        if self.should_test_run_now():
            rtn = self.do_test()
            if self.send_notification:
                self.notify(rtn)


    def subscribe_channel(self, channels):
        for channel in channels:
            if channel in Channel.channels:
                self.subscribed_channels.add(channel)
                logger.info("%s subscribed to %s" % (self, channel))
            else:
                logger.critical("Failed to find channel: %s" % channel)

    def failed(self, msg="Something failed"):
        if self.subscribed_channels:
            logger.info("%s failed with: %s. Sending notification via %s" % (self, msg, ', '.join(self.subscribed_channels)))
            for sc in self.subscribed_channels:
                if sc in Channel.available_channels:
                    obj = Channel.available_channels.get(sc)
                    obj.send_msg(msg)
                else:
                    logger.critical("Error! %s does not exist as a propery in the Channel class!" % (sc))
        else:
            logger.critical("%s failed with: %s. No notification being sent since there is no subscribed channels." % (self, msg))


    def notify(self, msg):
        if self.subscribed_channels:
            for sc in self.subscribed_channels:
                if sc in Channel.available_channels:
                    obj = Channel.available_channels.get(sc)
                    obj.send_msg(msg)
        else:
            logger.critical("%s failed with: %s. No notification being sent since there is no subscribed channels." % (self, msg))


    def passed(self, msg=""):
        pass_str = (str(self) or self.title) + " passed."

        for sc in self.subscribed_channels:
            if sc in Channel.available_channels:
                obj = Channel.available_channels.get(sc)
                if msg:
                    logger.info(msg)
                else:
                    logger.info(pass_str)

    def script_failed(self, msg):
        logger.info("Script failed to load: ", msg)
        return False

    def make_seconds(self, seconds):
        return int(seconds.replace("s", ""))

    def should_test_run_now(self):

        #Run every Xs
        if re.match("^[0-9]+s$", self.runtime):
            if int(time.time()) - self.last_run_time > self.make_seconds(self.runtime):
                self.last_run_time = time.time()
                return True

        #Run at HH:MM:SS
        elif re.match("^[0-9]{2}:[0-9]{2}:[0-9]{2}$", self.runtime):
            print time.strftime('%H:%M:%S'), "-", self.runtime
            if str(time.strftime('%H:%M:%S')) == self.runtime:
                return True
