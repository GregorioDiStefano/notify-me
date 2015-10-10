from channels import Channel
class LogFile(Channel):

    filename = "log.txt"

    def __init__(self, **kwargs):
        super(LogFile, self).__init__()

    def __str__(self):
        return "%s: writing to %s" % (self.name, self.filename)

    def do_send_msg(self, msg):
        with open(self.filename, "a") as myfile:
            myfile.write(msg)
