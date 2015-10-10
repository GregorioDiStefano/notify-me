from channel_importer import ChannelImporter
import script_importer
import threading
import time
import logging
import coloredlogs

coloredlogs.install(level=logging.DEBUG)

script_importer.do_import("scripts", globals())
tests = []


def scheduler():
    while True:
        try:
            for test in tests:
                t = threading.Thread(target=test.do, args=(), kwargs={})
                t.start()
            logging.debug("Active threads: %s" % threading.active_count())
            time.sleep(1)
        except KeyboardInterrupt:
            logging.debug("Exiting....")
            exit(0)

def import_channels():
    ci = ChannelImporter()


"""
    Lazy implementation for now
"""
def import_tests():
    tests.append(ping_test.Ping("8.8.8.8", max_avg_latency=50, runtime="20s", channel=["LogFile"]))
    #tests.append(shell_cmd.ShellCmd("ping -c 10 google.ca", runtime="1s", debug=True))
    #tests.append(shell_cmd.ShellCmd("ping -c 1 reddit.com", runtime="1s", ))
    tests.append(socket_open.OpenSocket(host="www.google.ca", ports=[80, 443, 4221], runtime="10s", channel=["LogFile", "Pushover"]))

if __name__ == "__main__":
    for script in script_importer.imported_scripts:
        logging.debug("Loaded: " + script)

    import_channels()
    import_tests()
    scheduler()
