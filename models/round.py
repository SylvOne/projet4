import datetime

class Round:
    def __init__(self, name, matches):
        self.name = name
        self.start_datetime = datetime.datetime.now()
        self.end_datetime = None
        self.matches = matches

