import json
import random
from models import Tournament, Player, Round
from utils import load_players_to_json, save_new_tournament, is_valid_start_date_tournament, is_valid_end_date_tournament, rm_accent_punct_space, file_manager
import os
from datetime import datetime
from views import tournament_views


def create_tournament():
    name = input("Entrez le nom du tournoi ")
    location = input("Entrez le lieu du tournoi ")

    while True:
        start_date = input("Entrez la date de début du tournoi (JJ/MM/AAAA) : ")
        if is_valid_start_date_tournament(start_date):
            break
    start_date_obj = datetime.strptime(start_date, '%d/%m/%Y')

    while True:
        end_date = input("Entrez la date de fin du tournoi (JJ/MM/AAAA) : ")
        if is_valid_end_date_tournament(end_date, start_date_obj):
            break

    num_rounds = input("Entrez le nombre de tours (Appuyez sur Entrée pour utiliser la valeur par défaut de 4) : ")
    if num_rounds == "":
        num_rounds = 4
    else:
        while not num_rounds.isnumeric() or int(num_rounds) < 1:
            print("Erreur : entrée non valide, veuillez entrer un entier supérieur ou égal à 1.")
            num_rounds = input("Entrez le nombre de tours (Appuyez sur Entrée pour utiliser la valeur par défaut de 4) : ")
        num_rounds = int(num_rounds)

    description = input("Entrez une description du tournoi ")

    # On Vérifie si un fichier "players.txt" est bien existant
    path_players = os.path.join('data', 'players', 'players.txt')
    if not os.path.isfile(path_players):
        print("Vous devez d'abord ajouter des participants avant de créer un tournoi")
        print("")
    else:

        # charger les joueurs pour la création d'un tournoi
        # path_players = os.path.join('data', 'players', 'players.txt')
        players = load_players_to_json(path_players)
        tournament = Tournament(name, location, start_date, end_date, num_rounds, description)

        for player in players:
            tournament.add_player(player)

        # Save tournament to json in ./data/tournaments
        tournament_file_name = str(int(datetime.strptime(tournament.start_date, '%d/%m/%Y').timestamp()))+"-"+str(int(datetime.strptime(tournament.end_date, '%d/%m/%Y').timestamp()))+"-"+rm_accent_punct_space(tournament.name)+".txt"
        path_tournament = os.path.join('data', 'tournaments', tournament_file_name)
        data_tournament = tournament.export_data_tournament()
        players_to_json = []
        for player in data_tournament['players']:
            players_to_json.append(player)
        # Création du nouveau dictionnaire avec les mêmes clés que les dictionnaires précédents
        data_tournament_to_json = {}
        for key in data_tournament.keys():
            if key == "players":
                data_tournament_to_json[key] = players_to_json
            else:
                data_tournament_to_json[key] = data_tournament[key]
        save_new_tournament(path_tournament, data_tournament_to_json, path_players)


def start_round_tournament():
    # On commence par afficher la liste des tournois en cours (c'est à dire, les tounois dont la date de début est égale ou antérieur à la date actuelle)
    path_directory = os.path.join('data', 'tournaments')
    paths_tournaments = file_manager.get_files_with_start_date_in_progress(path_directory)
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
            tournament.current_round = json_tournament["current_round"]
            tournament.pairs_to_do = json_tournament["matches"]

            # Add the players to the tournament
            players = []
            # on recupere les rounds du json tournament
            for player_data in json_tournament["players"]:
                players.extend(file_manager.load_players_to_json(player_data, json_tournament["players"]))

            tournament.players = players

            # on recupere les rounds du json tournament
            id_to_player = {player.national_id: player for player in players}
            tournament.rounds = []
            for round_data in json_tournament["rounds"]:
                round_ = Round(
                    name=round_data["name"],
                    matches=[]
                    # Nous devons charger les matches à partir des données JSON. Je laisse cette partie vide pour le moment.
                )
                round_.start_datetime = datetime.fromisoformat(round_data["start_time"])
                if round_data["end_time"]:
                    round_.end_datetime = datetime.fromisoformat(round_data["end_time"])


                round_.matches = [
                    (
                        [id_to_player[match_data["player1"]], match_data["player1_score"]],
                        [id_to_player[match_data["player2"]], match_data["player2_score"]],
                    )
                    for match_data in round_data["matches"]
                ]

                tournament.rounds.append(round_)

            # Ajout du tournoi à la liste des tournois en cours
            tournaments.append(tournament)
    print("")
    print("         ------------------------------")
    print("         | Liste des tournois en cours |")
    print("         ------------------------------")
    print("")
    tournament_views.display_tournaments(tournaments)

    while True:
        choice_tournament = input(" ==> Sélectionnez le numéro du tournoi que vous voulez lancer ('q' pour quitter)")
        if choice_tournament =='q':
            break
        # On vérifie la valeur entrée
        while not int(choice_tournament) <= len(tournaments):
            choice_tournament = input(" ==> La valeur entrée n'est pas correcte, veuillez entrer le numéro correspondant à un tournoi dans la liste ci-dessus :")

        # on récupère l'objet Tournoi selectionné
        selected_tournament = tournaments[int(choice_tournament)-1]

        # Lancement des tours d'un tournoi
        for _ in range(selected_tournament.num_rounds):
            if selected_tournament.start_round() == False:
                print("Le nombre de tours maximum a été atteint. Vous ne pouvez plus lancer ce tournoi")
                break
            current_round = selected_tournament.rounds[-1]

            print(f"\n{current_round.name} commencé à {current_round.start_datetime}")


            for match in current_round.matches:
                print(f"  {match[0][0].first_name} vs {match[1][0].first_name}")

            # Lancement des matchs
            count_match = 0
            stop_or_no = ""
            for match in current_round.matches:
                print(f" Entrez le résultat du match {match[0][0].first_name} vs joueur 2 : {match[1][0].first_name} :")
                print(f"joueur 1 : {match[0][0].first_name} {match[0][0].score}")
                print(f"joueur 2 : {match[1][0].first_name} {match[0][0].score}")
                print("==> Tapez 1. Le joueur 1 gagne.")
                print("==> Tapez 2. Le joueur 2 gagne.")
                print("==> Tapez 0. Pour match nul.")
                result = input("")
                result = int(result)
                if result == 1:
                    match[0][0].score += 1
                    match[0][1] = 1
                    match[1][1] = 0
                elif result == 2:
                    match[1][0].score += 1
                    match[1][1] = 1
                    match[0][1] = 0
                else:
                    match[0][0].score += 0.5
                    match[1][0].score += 0.5
                    match[0][1] = 0.5
                    match[1][1] = 0.5

                count_match += 1
                stop_or_no = input("Voulez-vous quitter et enregistrer le tournoi ? y: Oui , n: Non ")
                if stop_or_no == "y":
                    # On indique une variable booleene à la fonction save_existing_tournament() afin de savoir si tous les tours du tournoi ont été effecutés
                    finish_tournament = False
                    # on incremente de +1 la propriété current_round de la classe Tournament par contre ici on fait bien attention avant d'incrémenter d'avoir fini tous les matchs d'un tour
                    if count_match == len(current_round.matches):
                        selected_tournament.current_round += 1
                    # On enregistre au format json le tournoi
                    data_selected_tournament = selected_tournament.export_data_tournament()
                    path_of_tournament = paths_tournaments[int(choice_tournament) - 1]
                    # on enregistre les matchs dans pairs_to_do en vue d'enregistrer les matchs restant à faire si l'utilisateur quitte en cours de tour
                    if count_match < len(current_round.matches):
                        element = len(current_round.matches) - count_match
                        selected_tournament.pairs_to_do = current_round.matches[-element:]
                        # On enregistre au format json le tournoi
                        data_selected_tournament = selected_tournament.export_data_tournament()
                        path_of_tournament = paths_tournaments[int(choice_tournament) - 1]
                    if count_match == len(current_round.matches) and selected_tournament.current_round == selected_tournament.num_rounds:
                        finish_tournament = True
                    file_manager.save_existing_tournament(path_of_tournament ,data_selected_tournament, finish_tournament)
                    #selected_tournament.pairs_to_do = []
                    exit()

            if count_match == len(current_round.matches) and stop_or_no != "y":
                selected_tournament.end_round()
                print(f"{current_round.name} fini à {current_round.end_datetime}")
                # on incremente de +1 la propriété current_round de la classe Tournament
                selected_tournament.current_round += 1
                # on enregistre au format json le tournoi
                data_selected_tournament = selected_tournament.export_data_tournament()
                path_of_tournament = paths_tournaments[int(choice_tournament) - 1]
                # On indique une variable booleene à la fonction save_existing_tournament() afin de savoir si tous les tours du tournoi ont été effecutés
                finish_tournament = False
                if selected_tournament.current_round == selected_tournament.num_rounds:
                    finish_tournament = True
                print(selected_tournament.current_round)
                file_manager.save_existing_tournament(path_of_tournament, data_selected_tournament, finish_tournament)


