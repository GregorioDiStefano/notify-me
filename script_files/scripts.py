from abc import ABCMeta, abstractmethod
import time
import re
import logging

class Scripts(object):
    __metaclass__ = ABCMeta
    title = "This is the title"
    description = "This is the description"
    retries = 4
    runtime = "5s"
    debug = False

    last_run_time = int(time.time())

    def __init__(self, **kwargs):
        if "runtime" in kwargs:
            self.runtime = kwargs["runtime"]
        if "debug" in kwargs:
            self.debug = kwargs["debug"]

    @abstractmethod
    def do_test(self):
        pass

    def do(self):
        if self.should_test_run_now():
            self.do_test()

    def failed(self, msg = ""):
        logging.info("Failed with: %s. Sending notification." % msg)

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
