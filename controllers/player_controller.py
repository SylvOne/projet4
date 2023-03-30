import json
from main import main_menu
from utils import input_validation, file_manager
from models import Player, Tournament
from views import tournament_views
import os

def add_player_to_database():
    while True:
        first_name = input("Quel est le prénom du participant ?")
        last_name = input("Quel est le nom du participant ?")

        birth_date = input("Quelle est la date de naissance du participant ?")
        national_id = input("Quelle est l'identifiant national du participant ?")
        while not input_validation.is_valid_date(birth_date):
            birth_date = input("Quelle est la date de naissance du participant ?")
        while not input_validation.is_valid_national_id(national_id):
            national_id = input("Quelle est l'identifiant national du participant ?")

        # charger les données utilisateur dans le fichier
        player = Player(last_name, first_name, birth_date, national_id)
        data_player = player.export_data_player()
        path = os.path.join('data', 'players', 'players.txt')
        file_manager.save_player(path, data_player)

        again_or_menu = input("Voulez-vous ajouter un autre participant (1) ou revenir au menu principal (0) ? ")
        while again_or_menu not in ['0', '1']:
            again_or_menu = input("Voulez-vous ajouter un autre participant (1) ou revenir au menu principal (0) ? ")

        if again_or_menu == '0':
            break

    main_menu()

def add_players_tournament():
    # On commence par afficher la liste des tournois à venir
    path_directory = os.path.join('data', 'tournaments')
    paths_tournaments = file_manager.get_files_with_start_date_in_future(path_directory)
    tournaments = []
    for path_tournament in paths_tournaments:
        with open(path_tournament, "r", encoding='utf-8') as f:
            json_tournament = json.load(f)

            # Create an object of the Tournament class
            tournament = Tournament(
                json_tournament["name"],
                json_tournament["location"],
                json_tournament["start_date"],
                json_tournament["end_date"],
                json_tournament["num_rounds"],
                json_tournament["description"]
            )

            # Add the players to the tournament
            for player_data in json_tournament["players"]:
                player = Player(
                    player_data["last_name"][0],
                    player_data["first_name"][0],
                    player_data["date_of_birth"][0],
                    player_data["national_id"][0]
                )
                tournament.add_player(player)

            #Add tournament to the tournaments list
            tournaments.append(tournament)
    print("")
    print("         ------------------------------")
    print("         | Liste des tournois à venir |")
    print("         ------------------------------")
    tournament_views.display_tournaments(tournaments)