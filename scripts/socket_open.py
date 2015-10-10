from scripts import Scripts
from socket import socket

class OpenSocket(Scripts):
    host = ""
    ports = []

    def __init__(self, host, ports, **kwargs):
        self.title = "%s: %s open port check" % (host, ports)
        self.description = "Check if ports are open"
        self.host = host
        self.ports = ports

        #pass remaining arguments to the parent class
        super(OpenSocket, self).__init__(**kwargs)

    def do_test(self):
        for port in self.ports:
            try:
                s = socket()
                s.settimeout(1)
                s.connect( (self.host, int(port)) )
            except Exception, e:
                fail_str = "%s:%d is closed" % (self.host, port)
                self.failed(fail_str)
            else:
                self.passed("%s:%d is opened" % (self.host, port))
