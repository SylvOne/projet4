class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.score = 0
        self.opponents = []

    def update_score(self, points):
        self.score += points

    def export_data_player(self):
        player_data = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "score": self.score,
            "opponents": [opponent.national_id for opponent in self.opponents]
        }
        return player_data

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.score})"
