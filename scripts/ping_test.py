from scripts import Scripts
import subprocess
import re
import logging

class Ping(Scripts):
    host = ""
    max_avg_latency = ""

    def __init__(self, host, max_avg_latency=False, **kwargs):
        self.title = "Ping test"
        self.description = "Ping test"
        self.host = host
        self.max_avg_latency = max_avg_latency

        #pass remaining arguments to the parent class
        super(Ping, self).__init__(**kwargs)

    def __str__(self):
        return "<Ping Test for : %s>" % (self.host)

    def do_test(self):
        ping = subprocess.Popen(
            ["ping", "-c", "10", self.host],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = ping.communicate()
        exit_code = ping.returncode

        if error or exit_code:
            if self.debug:
                logging.debug("%s failed with: %s" % (self.title, error))
            self.failed()

        elif self.max_avg_latency:
            last_line = out.strip().split('\n')[-1]
            if "rtt min/avg/max/mdev" in last_line:
                avg = float(last_line.split('=')[1].strip().split('/')[1])
                if avg > self.max_avg_latency:
                    self.failed("avg ping time is: %f, expected: < %f" % (avg, self.max_avg_latency))
            else:
                self.failed("%s: unexpected ping output!" % (self))
        else:
            self.passed()
