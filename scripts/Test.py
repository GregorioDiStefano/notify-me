from Scripts import Scripts

class Test(Scripts):
    def __init__(self):
        self.description = "Overrode description"
        print "Hello", self.description

    def pass_condition(self):
        pass
