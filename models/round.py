class Round:
    def __init__(self, name):
        self.name = name
        self.start_datetime = None
        self.end_datetime = None
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)

    def start(self, datetime):
        self.start_datetime = datetime

    def end(self, datetime):
        self.end_datetime = datetime
