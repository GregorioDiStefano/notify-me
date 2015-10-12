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

    def __str__(self):
        return "<%s:%s>" % (self.host, " ".join(self.ports))

    def do_test(self):
        for port in self.ports:
            try:
                s = socket()
                s.settimeout(1)
                s.connect( (self.host, int(port)) )
            except Exception, e:
                self.failed(str(self) + ":" + str(e))
            else:
                self.passed()
