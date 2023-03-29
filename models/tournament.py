class Tournament:
    def __init__(self, name, location, start_date, end_date, num_rounds=4, description=""):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.current_round = 0
        self.rounds = []
        self.players = []
        self.description = description

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round):
        self.rounds.append(round)
        self.current_round += 1

    def export_data_tournament(self):
        tournament_data = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "num_rounds": self.num_rounds,
            "current_round": self.current_round,
            "rounds": self.rounds,
            "players": self.players,
            "description": self.description
        }
        return tournament_data
