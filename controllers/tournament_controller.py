from models import Tournament
from utils import file_manager, input_validation, string_manager
import os
from datetime import datetime
from views import tournament_views


def create_tournament():
    name = input("Entrez le nom du tournoi ")
    location = input("Entrez le lieu du tournoi ")

    while True:
        start_date = input("Entrez la date de début du tournoi (JJ/MM/AAAA) : ")
        if input_validation.is_valid_start_date_tournament(start_date):
            break
    start_date_obj = datetime.strptime(start_date, '%d/%m/%Y')

    while True:
        end_date = input("Entrez la date de fin du tournoi (JJ/MM/AAAA) : ")
        if input_validation.is_valid_end_date_tournament(end_date, start_date_obj):
            break

    num_rounds = input("Entrez le nombre de tours (Appuyez sur Entrée pour utiliser la valeur par défaut de 4) : ")
    if num_rounds == "":
        num_rounds = 4
    else:
        while not num_rounds.isnumeric() or int(num_rounds) < 1:
            print("Erreur : entrée non valide, veuillez entrer un entier supérieur ou égal à 1.")
            num_rounds = input("Entrez le nombre de tours "
                               "(Appuyez sur Entrée pour utiliser la valeur par défaut de 4) : ")
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
        players = file_manager.load_players_to_json(path_players)
        tournament = Tournament(name, location, start_date, end_date, num_rounds, description)

        for player in players:
            tournament.add_player(player)

        # Save tournament to json in ./data/tournaments
        start_date_timestamp = int(datetime.strptime(tournament.start_date, '%d/%m/%Y').timestamp())
        end_date_timestamp = int(datetime.strptime(tournament.end_date, '%d/%m/%Y').timestamp())
        clean_tournament_name = string_manager.rm_accent_punct_space(tournament.name)
        tournament_file_name = (
            f"{start_date_timestamp}-{end_date_timestamp}-{clean_tournament_name}.txt"
        )
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
        file_manager.save_new_tournament(path_tournament, data_tournament_to_json, path_players)


def start_round_tournament():
    path_directory = os.path.join('data', 'tournaments')
    tournaments = file_manager.load_tournaments_in_progress(path_directory)

    tournament_views.display_tournaments_in_progress(tournaments)

    selected_tournament = file_manager.get_selected_tournament(tournaments)
    if not selected_tournament:
        return

    # Lancement des tours d'un tournoi
    start_date = datetime.strptime(selected_tournament.start_date, '%d/%m/%Y')
    end_date = datetime.strptime(selected_tournament.end_date, '%d/%m/%Y')

    start_date_timestamp = int(start_date.timestamp())
    end_date_timestamp = int(end_date.timestamp())
    filename = (
        f"{start_date_timestamp}-{end_date_timestamp}-"
        f"{string_manager.rm_accent_punct_space(selected_tournament.name)}.txt"
    )

    path_of_tournament = os.path.join('data', 'tournaments', filename)
    for _ in range(selected_tournament.num_rounds):
        if selected_tournament.start_round() is False:
            print("Le nombre de tours maximum a été atteint. Vous ne pouvez plus lancer ce tournoi")
            break
        current_round = selected_tournament.rounds[-1]

        print(f"\n{current_round.name} commencé à {current_round.start_datetime}")

        for match in current_round.matches:
            print(f"  {match.match[0][0].first_name} vs {match.match[1][0].first_name}")

        # Lancement des matchs
        count_match = 0
        stop_or_no = ""
        for match in current_round.matches:
            print(f" Entrez le résultat du match {match.match[0][0].first_name} vs {match.match[1][0].first_name} :")
            print(f"joueur 1 : {match.match[0][0].first_name} score actuel => {match.match[0][0].score}")
            print(f"joueur 2 : {match.match[1][0].first_name} score actuel => {match.match[1][0].score}")
            print("==> Tapez 1. Le joueur 1 gagne.")
            print("==> Tapez 2. Le joueur 2 gagne.")
            print("==> Tapez 0. Pour match nul.")
            result = input("")
            result = int(result)
            if result == 1:
                match.match[0][0].score += 1
                match.match[0][1] = 1
                match.match[1][1] = 0
            elif result == 2:
                match.match[1][0].score += 1
                match.match[1][1] = 1
                match.match[0][1] = 0
            else:
                match.match[0][0].score += 0.5
                match.match[1][0].score += 0.5
                match.match[0][1] = 0.5
                match.match[1][1] = 0.5

            count_match += 1
            stop_or_no = input("Voulez-vous quitter et enregistrer le tournoi ? y: Oui , n: Non ")
            if stop_or_no == "y":
                # On indique une variable booleene à la fonction save_existing_tournament()
                # afin de savoir si tous les tours du tournoi ont été effecutés
                finish_tournament = False
                # on incremente de +1 la propriété current_round de la classe Tournament
                # par contre ici on fait bien attention avant d'incrémenter d'avoir fini tous les matchs d'un tour
                if count_match == len(current_round.matches):
                    selected_tournament.current_round += 1
                # On enregistre au format json le tournoi
                data_selected_tournament = selected_tournament.export_data_tournament()

                # on enregistre les matchs dans pairs_to_do
                # en vue d'enregistrer les matchs restant à faire si l'utilisateur quitte en cours de tour
                if count_match < len(current_round.matches):
                    element = len(current_round.matches) - count_match
                    selected_tournament.pairs_to_do = current_round.matches[-element:]
                    # On enregistre au format json le tournoi
                    data_selected_tournament = selected_tournament.export_data_tournament()
                # Si le compteur de match est égale au nombre de matches du tour
                # et que le tour actuel est le dernier tour alors le tournoi est fini
                if (count_match == len(current_round.matches) and
                        selected_tournament.current_round == selected_tournament.num_rounds):
                    finish_tournament = True
                if count_match == len(current_round.matches):
                    selected_tournament.end_round()
                file_manager.save_existing_tournament(path_of_tournament, data_selected_tournament, finish_tournament)
                exit()

        if count_match == len(current_round.matches) and stop_or_no != "y":
            selected_tournament.end_round()
            print(f"{current_round.name} fini à {current_round.end_datetime}")
            # on incremente de +1 la propriété current_round de la classe Tournament
            selected_tournament.current_round += 1
            # on enregistre au format json le tournoi
            data_selected_tournament = selected_tournament.export_data_tournament()

            # On indique une variable booleene à la fonction save_existing_tournament()
            # afin de savoir si tous les tours du tournoi ont été effecutés
            finish_tournament = False
            if selected_tournament.current_round == selected_tournament.num_rounds:
                finish_tournament = True
            file_manager.save_existing_tournament(path_of_tournament, data_selected_tournament, finish_tournament)
