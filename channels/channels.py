import logging

logger = logging.getLogger("notifyme")

class Channel(object):

    name = ""
    channels = set()
    channel_name = ""


    # The following are static variable set by ChannelImporter
    available_channels = dict()

    def __init__(self):
        self.channel_name = self.__class__.__name__
        Channel.register_channel(self.channel_name, self)
        logger.debug("Loaded: %s", self)

    @staticmethod
    def register_channel(channel_name, obj):
        Channel.channels.add(channel_name)
        Channel.available_channels[channel_name] = obj

    def send_msg(self, msg):
        self.do_send_msg(msg)
