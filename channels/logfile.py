from channels import Channel
import datetime

class LogFile(Channel):

    filename = "log.txt"
    log_passes = True

    def __init__(self, **kwargs):
        super(LogFile, self).__init__()

    def __str__(self):
        return "<%s> writing to %s" % (self.channel_name, self.filename)

    def do_send_msg(self, msg):
        with open(self.filename, "a") as myfile:
            msg_prefix =  str(datetime.datetime.now())
            myfile.write(msg_prefix + ": " + msg + "\n")
