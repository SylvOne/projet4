from models.round import Round
import random
import datetime
from models.match import Match


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
        self.pairs_to_do = []

    def add_player(self, player):
        self.players.append(player)

    def generate_pairs(self):
        players = self.players.copy()
        random.shuffle(players)
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        pairs = []

        if self.pairs_to_do:
            for joueur in self.pairs_to_do:
                player1_id = joueur["player1"]
                player2_id = joueur["player2"]

                for i, player in enumerate(sorted_players):
                    if (player.national_id == player1_id and
                            i + 1 < len(sorted_players) and sorted_players[i + 1].national_id == player2_id):
                        match = Match(player, sorted_players[i + 1])
                        pairs.append(match)
                        break
            # On vide la propriété pairs_to_do
            self.pairs_to_do = []
        else:
            # Si le nombre de joueurs est impaire alors on retire un joueur de la liste de joueurs
            # Ce joueur sera choisi s'il n'est pas lui meme inscrit dans le dernier élement de sa liste d'opposants.
            # De ce fait, si les conditions sont remplis et qu'on le choisi comme bye player
            # alors on le retire de la liste de joueurs initiale et on l'ajoute à sa liste d'opposants
            # Cela permet d'être sur de ne pas choisir par mal chance toujours le meme joueurs
            if len(sorted_players) % 2 == 1:
                for player in sorted_players:
                    if len(player.opponents) == 0 or player.opponents[-1] != player:
                        player.opponents.append(player)
                        sorted_players.remove(player)
                        break

            for i in range(0, len(sorted_players), 2):
                player1 = sorted_players[i]
                player2 = sorted_players[i + 1]

                while player2 in player1.opponents:
                    i += 1
                    if i + 1 >= len(sorted_players):
                        break
                    player2 = sorted_players[i + 1]

                match = Match(player1, player2)
                pairs.append(match)
                player1.opponents.append(player2)
                player2.opponents.append(player1)

        return pairs

    def start_round(self):
        if self.current_round < self.num_rounds:
            round_name = f"Tour {self.current_round + 1}"
            round_matches = self.generate_pairs()
            new_round = Round(round_name, round_matches)
            self.rounds.append(new_round)
            return True
        else:
            return False

    def end_round(self):
        self.rounds[-1].end_datetime = datetime.datetime.now()

    def export_data_tournament(self):
        tournament_data = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "num_rounds": self.num_rounds,
            "current_round": self.current_round,
            "rounds": [
                {
                    "name": round_.name,
                    "matches": [
                        {
                            "player1": match.match[0][0].national_id,
                            "player1_score": match.match[0][1],
                            "player2": match.match[1][0].national_id,
                            "player2_score": match.match[1][1],
                        }
                        for match in round_.matches
                    ],
                    "start_time": round_.start_datetime.isoformat(),
                    "end_time": round_.end_datetime.isoformat() if round_.end_datetime else None,
                }
                for round_ in self.rounds
            ] if self.rounds else self.rounds,
            "players": (
                [player.export_data_player() for player in self.players] if len(self.players) > 1 else self.players
            ),
            "description": self.description,
            "matches": [
                {
                    "player1": match.match[0][0].national_id,
                    "player2": match.match[1][0].national_id,
                }
                for match in self.pairs_to_do
            ],

        }
        return tournament_data

    def __repr__(self):
        return f"{self.name} - {self.location} ({self.start_date} - {self.end_date})"
