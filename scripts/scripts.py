from abc import ABCMeta, abstractmethod
import time
import re
import logging
import sys

sys.path.append("..")
from channels.channels import Channel

class Scripts(object):
    __metaclass__ = ABCMeta
    title = "This is the title"
    description = "This is the description"
    retries = 4
    runtime = "5s"
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

    @abstractmethod
    def do_test(self):
        pass

    def do(self):
        if self.should_test_run_now():
            self.do_test()

    def subscribe_channel(self, channels):
        for channel in channels:
            logging.debug("Subscribing %s to: %s" % (self, channel))
            if channel in Channel.channels:
                self.subscribed_channels.add(channel)
                logging.info("%s subscribed to %s" % (self, channel))
            else:
                logging.critical("Failed to find channel: %s" % channel)

    def failed(self, msg = ""):
        logging.info("Failed with: %s. Sending notification via %s" % (msg, self.subscribed_channels))
        for sc in self.subscribed_channels:
            if sc in Channel.available_channels:
                obj = Channel.available_channels.get(sc)
                obj.send_msg(msg)
            else:
                logging.critical("Error! %s does not exist as a propery in the Channel class!" % (sc))

    def passed(self):
        logging.info("Passed.")

    def script_failed(self, msg):
        logging.info("Script failed to load: ", msg)
        return False

    def make_seconds(self, seconds):
        return int(seconds.replace("s", ""))

    def should_test_run_now(self):

        #Run every Xs
        if re.match("^[0-9]+s$", self.runtime):
            if int(time.time()) - self.last_run_time > self.make_seconds(self.runtime):
                self.last_run_time = time.time()
                return True
