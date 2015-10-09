import script_importer
import threading
import time

script_importer.do_import("script_files", globals())
tests = []


for script in script_importer.imported_scripts:
    print "Loaded: ", script

tests.append(ping_test.Test("8.8.8.8", max_avg_latency=20, runtime="5s"))

while True:
    try:
        for test in tests:
            threading.Thread(target=test.do, args=(), kwargs={}).start()
        time.sleep(1)
    except KeyboardInterrupt:
        print "Exiting...."
        exit(0)
