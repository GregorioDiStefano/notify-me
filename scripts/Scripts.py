from abc import ABCMeta, abstractmethod

class Scripts(object):
    __metaclass__ = ABCMeta
    description="This is the description"
    
    @abstractmethod
    def pass_condition(self):
        pass
