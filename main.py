from channel_import import ChannelImporter
import script_import
import threading
import time
import logging
import coloredlogs
import sys
import inspect


script_settings_filename = "conf/scripts.json"
coloredlogs.install(level=logging.DEBUG)
script_import.do_import("scripts", globals())


def scheduler(tests):
    while True:
        try:
            for test in tests:
                t = threading.Thread(target=test.do, args=(), kwargs={})
                t.start()
            logging.debug("Active threads: %s" % threading.active_count())
            time.sleep(1)
        except KeyboardInterrupt:
            logging.debug("Exiting....")
            sys.exit(0)

def import_channels():
    ChannelImporter()

"""
    Lazy implementation for now
"""
def import_tests():
    return script_import.ScriptConfig(script_settings_filename).script_objects
    #tests.append(ping_test.Ping("8.8.8.8", max_avg_latency=50, runtime="20s", channel=["LogFile"]))
    #tests.append(shell_cmd.ShellCmd("ping -c 10 google.ca", runtime="1s", debug=True))
    #tests.append(shell_cmd.ShellCmd("ping -c 1 reddit.com", runtime="1s", ))
    #tests.append(socket_open.OpenSocket(host="www.google.ca", ports=[80, 443, 4221], runtime="10s", channel=["LogFile", "Pushover"]))

if __name__ == "__main__":
    logging.debug("Loaded: %s" % str(script_import.imported_classes))

    import_channels()
    tests = import_tests()
    scheduler(tests)
