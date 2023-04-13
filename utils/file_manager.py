import json
import os
import pytz as pytz
from models import Player, Tournament, Match
from models import Round
from datetime import datetime


def load_players_to_json(file_path, id_players=None):
    # on vérifie si c'est un fichier path ou directement de la data json
            # Vérifier si le fichier existe

    if isinstance(file_path, dict):
        players_data = [file_path]
    elif os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as infile:
            players_data = json.load(infile)
    elif "players.txt" in file_path:
        return False
    else:
        players_data = json.loads(file_path)

    players_all = []
    if id_players:
        for play_data in id_players:
            player = Player(
                play_data["last_name"],
                play_data["first_name"],
                play_data["date_of_birth"],
                play_data["national_id"]
            )
            player.score = play_data["score"]

            players_all.append(player)

    players = []
    for player_data in players_data:
        player = Player(
            player_data["last_name"],
            player_data["first_name"],
            player_data["date_of_birth"],
            player_data["national_id"]
        )
        player.score = player_data["score"]

        players.append(player)

    # On ajoute les adversaires à chaque joueur
    if id_players:
        id_to_player = {player.national_id: player for player in players_all}
        for player, player_data in zip(players, players_data):
            player.opponents = [id_to_player[opponent_id] for opponent_id in player_data["opponents"]]
    else:
        id_to_player = {player.national_id: player for player in players}
        for player, player_data in zip(players, players_data):
            player.opponents = [id_to_player[opponent_id] for opponent_id in player_data["opponents"]]

    return players


def save_player(file_path, players):
    players_data = [player.export_data_player() for player in players]
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(players_data, outfile, ensure_ascii=False)


def save_new_tournament(file_path, data, file_path_players):
    """
    This function check if the file "players.txt" exist and check if the tournament does not already exist, and if
    it's ok, it create a new tournament file in .data/tournament, and rename the file "players.txt" to
    'start_date_tournament-end_date_tournament-NameTournament.txt"

    :param file_path: This is a filepath to create a new tournament file and to check if this file does not already exist.
    :param data: This json data tournament to record in .txt file.
    :param file_path_players: This is a players filepath (players.txt) to check if this file exist in ./data/players
    """
    from main import main_menu
    # On Vérifie si un fichier tournoi existe, ensuite on vérifie si un fichier "players.txt" est bien existant
    if os.path.isfile(file_path):
        print("Un tournoi identique est déjà existant")
    elif not os.path.isfile(file_path_players):
        print("Vous devez d'abord ajouter des participants avant de créer un tournoi")
    else:
        # Si le tournoi n'existe pas, on créer un nouveau fichier tournoi
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        # On prépare le nouveau chemin et nom du fichier "players.txt" qui deviendra "start_date_timestamp_players.txt"
        new_path = file_path.replace("tournaments", "players")

        # Et maintenant on renomme le fichier players.txt
        os.rename(file_path_players, new_path)
    main_menu()


def save_existing_tournament(file_path, data, finish_tournament = False):
    """
    This function update tournament file in .data/tournament

    :param file_path: This is a filepath to create a new tournament file and to check if this file does not already exist.
    :param data: This is json data tournament to record in .txt file.
    """
    from main import main_menu
    # On Vérifie si un fichier tournoi existe, ensuite on vérifie si un fichier "players.txt" est bien existant
    if os.path.isfile(file_path):
        # Si le tous les tours du tournoi ont été effectué alors on inscrit finished à la fin du fichier texte correspondant au tournoi
        # on modifie également le nom du fichier joueurs texte en ajoutant "finished" (data/players/nomdufichier-finished)
        if finish_tournament:
            # Je supprimer l'ancien fichier tournoi sans le "finished"
            os.remove(file_path)
            # je récupère le chemin de mon fichier texte de joueurs correspondant au tournoi en question
            old_file_path_players = file_path.replace("tournaments", "players")
            # J'ajoute le mot "finished" au nom du fichier tournoi et je réaffecte la valeur de file_path
            parts = file_path.rsplit(".", 1)
            file_path = f"{parts[0]}-finished.{parts[1]}"
            # On prépare le nouveau chemin et nom du fichier joueur
            new_path_players = file_path.replace("tournaments", "players")
            # Et maintenant on renomme le fichier players.txt
            os.rename(old_file_path_players, new_path_players)

        #  on créer un nouveau fichier tournoi
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    else:
        # Si le tournoi n'existe pas, on créer un nouveau fichier tournoi
        print("Le tournoi n'existe pas")
    #main_menu()


def load_tournaments_in_progress(path_directory):
    paths_tournaments = get_files_with_start_date_in_progress(path_directory)
    tournaments = []
    for path_tournament in paths_tournaments:
        tournament = load_tournament_from_file(path_tournament)
        tournaments.append(tournament)
    return tournaments


def load_tournament_from_file(path_tournament):
    with open(path_tournament, "r", encoding='utf-8') as f:
        json_tournament = json.load(f)

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

    players = load_players(json_tournament)
    tournament.players = players

    id_to_player = {player.national_id: player for player in players}
    rounds = load_rounds(json_tournament, id_to_player)
    tournament.rounds = rounds

    return tournament


def load_players(json_tournament):
    players = []
    for player_data in json_tournament["players"]:
        players.extend(load_players_to_json(player_data, json_tournament["players"]))
    return players


def load_rounds(json_tournament, id_to_player):
    rounds = []
    for round_data in json_tournament["rounds"]:
        round_ = Round(
            name=round_data["name"],
            matches=[]
        )
        round_.start_datetime = datetime.fromisoformat(round_data["start_time"])
        if round_data["end_time"]:
            round_.end_datetime = datetime.fromisoformat(round_data["end_time"])
        matches = []
        for match_data in round_data["matches"]:
            match = Match(id_to_player[match_data["player1"]], id_to_player[match_data["player2"]])
            match.match[0][1] = match_data["player1_score"]
            match.match[1][1] = match_data["player2_score"]
            matches.append(match)

        round_.matches = matches
        rounds.append(round_)

    return rounds


def get_selected_tournament(tournaments):
    while True:
        choice_tournament = input(" ==> Sélectionnez le numéro du tournoi que vous voulez lancer ('q' pour quitter)")
        if choice_tournament == 'q':
            return None
        while not int(choice_tournament) <= len(tournaments):
            choice_tournament = input(" ==> La valeur entrée n'est pas correcte, veuillez entrer le numéro correspondant à un tournoi dans la liste ci-dessus :")

        selected_tournament = tournaments[int(choice_tournament) - 1]
        return selected_tournament


def get_files_with_start_date_in_future(directory):
    # Récupération de la date actuelle en timestamp
    timezone = pytz.timezone('Europe/Paris')
    today = datetime.now(timezone).date()

    # Liste des fichiers dont la date de début est à venir
    future_files = []
    # Parcours des fichiers dans le répertoire donné
    for filename in os.listdir(directory):
        # Récupération de la date de début du tournoi à partir du nom du fichier
        start_date = int(filename.split("-")[0])
        # Convertir le timestamp en objet datetime avec le fuseau horaire UTC
        utc_dt = datetime.utcfromtimestamp(start_date).replace(tzinfo=pytz.utc)
        # Convertir le fuseau horaire UTC en fuseau horaire France
        convert_start_date = utc_dt.astimezone(timezone).date()
        # Si la date de début est à venir, et que le nom du fichier tournoi ne contient pas "finished" on ajoute le fichier à la liste
        if convert_start_date >= today and not "finished" in filename:
            future_files.append(os.path.join(directory, filename))
    return future_files

def get_files_with_start_date_in_progress(directory):
    # Récupération de la date actuelle en timestamp
    timezone = pytz.timezone('Europe/Paris')
    today = datetime.now(timezone).date()
    # Liste des fichiers dont la date de début est à venir
    progress_files = []
    # Parcours des fichiers dans le répertoire donné
    for filename in os.listdir(directory):
        if filename != ".DS_Store":
            # Récupération de la date de début du tournoi à partir du nom du fichier
            start_date = int(filename.split("-")[0])
            # Convertir le timestamp en objet datetime avec le fuseau horaire UTC
            utc_dt = datetime.utcfromtimestamp(start_date).replace(tzinfo=pytz.utc)
            # Convertir le fuseau horaire UTC en fuseau horaire France
            convert_start_date = utc_dt.astimezone(timezone).date()
            # Si la date de début est en cours par rapport à la date actuelle et que le tournoi n'est pas fini alors, on ajoute le fichier à la liste
            if convert_start_date == today and not "finished" in filename or convert_start_date < today and not "finished" in filename:
                progress_files.append(os.path.join(directory, filename))
    return progress_files