import script_importer
import threading
import time

script_importer.do_import("script_files", globals())
tests = []

for script in script_importer.imported_scripts:
    print "Loaded: ", script

tests.append(ping_test.Ping("8.8.8.8", max_avg_latency=20, runtime="5s"))
tests.append(shell_cmd.ShellCmd("ping -c 10 google.ca", runtime="1s"))
tests.append(shell_cmd.ShellCmd("ping -c 1 reddit.com", runtime="1s"))

while True:
    try:
        for test in tests:
            t = threading.Thread(target=test.do, args=(), kwargs={})
            t.start()
        time.sleep(1)
    except KeyboardInterrupt:
        print "Exiting...."
        exit(0)
