import json
import os
import time

import pytz as pytz

from models import Player
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



def load_round_json(round_json, players_by_id):
    name = round_json["name"]
    start_datetime = datetime.fromisoformat(round_json["start_time"])
    end_datetime = datetime.fromisoformat(round_json["end_time"]) if round_json["end_time"] else None

    matches = []
    for match_json in round_json["matches"]:
        player1 = players_by_id[match_json["player1_id"]]
        player1_score = match_json["player1_score"]
        player2 = players_by_id[match_json["player2_id"]]
        player2_score = match_json["player2_score"]
        matches.append(([player1, player1_score], [player2, player2_score]))

    round_ = Round(name, matches)
    round_.start_datetime = start_datetime
    round_.end_datetime = end_datetime

    return round_

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