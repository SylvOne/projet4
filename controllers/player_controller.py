import json
from main import main_menu
from utils import input_validation, file_manager
from models import Player, Tournament
from views import tournament_views
import os


def add_player_to_database():
    """
    Fonction permettant d'ajouter des joueurs en vue de créer un tournoi
    """

    players = []
    while True:
        first_name = input("Quel est le prénom du participant ?")
        last_name = input("Quel est le nom du participant ?")
        birth_date = input("Quelle est la date de naissance du participant ?")
        while not input_validation.is_valid_date(birth_date):
            birth_date = input("Quelle est la date de naissance du participant ?")
        national_id = input("Quelle est l'identifiant national du participant ?")
        while not input_validation.is_valid_national_id(national_id):
            national_id = input("Quelle est l'identifiant national du participant ?")

        # charger les données utilisateur dans le fichier
        player = Player(last_name, first_name, birth_date, national_id)
        players.append(player)
        path = os.path.join('data', 'players', 'players.txt')

        again_or_menu = input("Voulez-vous ajouter un autre participant (1) ou revenir au menu principal (0) ? ")
        while again_or_menu not in ['0', '1']:
            again_or_menu = input("Voulez-vous ajouter un autre participant (1) ou revenir au menu principal (0) ? ")

        if again_or_menu == '0':
            # Charger les joueurs existants
            existing_players = file_manager.load_players_to_json(path)

            # Fusionner les listes de joueurs
            if existing_players is not False:
                all_players = existing_players + players
                # Enregistrer tous les joueurs (anciens et nouveaux) dans le fichier
                file_manager.save_player(path, all_players)
            else:
                # Enregistrer tous les joueurs (anciens et nouveaux) dans le fichier
                file_manager.save_player(path, players)
            break

    main_menu()


def add_players_tournament():
    """
    Fonction permettant de rajouter des joueurs à un tournoi dont la date de début est à venir
    """

    # On commence par afficher la liste des tournois à venir
    path_directory = os.path.join('data', 'tournaments')
    paths_tournaments = file_manager.get_files_with_start_date_in_future(path_directory)
    if not paths_tournaments:
        while True:
            response = input("Vous devez avoir au moins un tournoi à venir pour réaliser cette action :"
                             " tapez 'q' pour quitter")
            if response == "q":
                main_menu()

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
            path_dir_players = path_tournament.replace("tournaments", "players")
            players = file_manager.load_players_to_json(path_dir_players)
            for player in players:
                tournament.add_player(player)

            # Add tournament to the tournaments list
            tournaments.append(tournament)
    print("")
    print("         ------------------------------")
    print("         | Liste des tournois à venir |")
    print("         ------------------------------")
    print("")
    tournament_views.display_tournaments(tournaments)

    while True:
        choice_tournament = input(
            "=> Sélectionnez le numéro du tournoi dans lequel "
            "vous désirez rajouter des participants ('q' pour quitter)"
        )
        if choice_tournament == 'q':
            break
        # On vérifie la valeur entrée
        while True:
            try:
                if not int(choice_tournament) <= len(tournaments):
                    choice_tournament = input(
                        "==> La valeur entrée n'est pas correcte, "
                        "veuillez entrer le numéro correspondant à un tournoi dans la liste ci-dessus :")
                else:
                    break
            except ValueError:
                print("Vous devez entrer un nombre entier")
                choice_tournament = input(
                    "=> Sélectionnez le numéro du tournoi dans lequel "
                    "vous désirez rajouter des participants ('q' pour quitter)"
                )
        # on récupère l'objet Tournoi selectionné
        selected_tournament = tournaments[int(choice_tournament) - 1]

        # On fait la demande d'ajout et l'enregistrement du ou des nouveaux participants pour le tournoi selectionné
        first_name = input("Quel est le prénom du participant ?")
        last_name = input("Quel est le nom du participant ?")

        birth_date = input("Quelle est la date de naissance du participant ?")
        national_id = input("Quelle est l'identifiant national du participant ?")
        while not input_validation.is_valid_date(birth_date):
            birth_date = input("Quelle est la date de naissance du participant ?")
        while not input_validation.is_valid_national_id(national_id):
            national_id = input("Quelle est l'identifiant national du participant ?")

        # On ajoute le nouveau joueur dans le fichier players portant le nom du tournoi
        path_given_tournament = paths_tournaments[int(choice_tournament) - 1]
        path = path_given_tournament.replace("tournaments", "players")
        # Charger les joueurs existants
        existing_players = file_manager.load_players_to_json(path)
        # le joueur à rajouter
        player = Player(last_name, first_name, birth_date, national_id)
        # Fusionner les listes de joueurs
        all_players = existing_players + [player]
        # Enregistrer tous les joueurs (anciens et nouveaux) dans le fichier
        file_manager.save_player(path, all_players)

        # On ajoute les nouveaux participants à l'objet Tournoi selectionné par l'utilisateur
        selected_tournament.add_player(player)

        # On demande si l'utilisateur veut rajouter d'autres participants ?
        again_or_menu = input("Voulez-vous ajouter un autre participant (1) ou revenir au menu principal (0) ? ")
        while again_or_menu not in ['0', '1']:
            again_or_menu = input("Voulez-vous ajouter un autre participant (1) ou revenir au menu principal (0) ? ")

        if again_or_menu == '0':
            # Avant de sortir du menu on enregistrer au format json l'objet Tournament avec les nouveaux players
            file_manager.save_existing_tournament(path_given_tournament, selected_tournament.export_data_tournament())
            break

    main_menu()
