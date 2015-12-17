#!/usr/bin/env python

from channel_import import ChannelImporter
import script_import
import threading
import time
import log
#import coloredlogs
import sys
import inspect
import os


script_settings_filename = os.path.dirname(os.path.abspath(__file__)) + "/conf/scripts.json"
#coloredlogs.install(level=logging.DEBUG)
script_import.do_import(os.path.dirname(os.path.abspath(__file__)) + "/scripts", globals())



def scheduler(tests):
    while True:
        try:
            for test in tests:
                t = threading.Thread(target=test.do, args=(), kwargs={})
                t.start()
            logger.debug("Active threads: %s" % (threading.active_count()))
            time.sleep(1)
        except KeyboardInterrupt:
            logger.debug("Exiting....")
            sys.exit(0)

def import_channels():
    ChannelImporter()

def import_tests():
    return script_import.ScriptConfig(script_settings_filename).script_objects

if __name__ == "__main__":
    logger = log.setup_custom_logger('notifyme')
    logger.debug("Loaded: %s" % str(script_import.imported_classes))

    import_channels()
    tests = import_tests()
    scheduler(tests)
