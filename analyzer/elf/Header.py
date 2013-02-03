class Header(object):


    def __init__(self):
        self.contents = {}

    def set(self, key, val):
        self.contents[key] = val

    def get(self, key):
        return self.contents[key]

    def echo(self):
        None
