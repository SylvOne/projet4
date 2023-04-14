class Match:
    def __init__(self, player1, player2):
        self.match = ([player1, 0], [player2, 0])

    def __repr__(self):
        return f"{self.match[0][0].first_name} vs {self.match[1][0].first_name} "
