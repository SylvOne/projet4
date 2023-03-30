import json
import os
import time


def load_players_to_json(file_path):
    # Vérifier si le fichier existe
    if os.path.isfile(file_path):
        # Si le fichier existe, ouvrir le fichier en mode lecture
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    else:
        print("Vous devez d'abord enregistrer des participants avant de créer un tournoi.")


def save_player(file_path, data):
    # Vérifier si le fichier existe
    if os.path.isfile(file_path):
        # Si le fichier existe, ouvrir le fichier en mode lecture
        with open(file_path, "r", encoding='utf-8') as f:
            existing_data = json.load(f)

        # Vérifier si l'utilisateur existe déjà
        if data['national_id'] not in existing_data['national_id']:
            # Ajouter le nouvel utilisateur
            # Création du nouveau dictionnaire avec les mêmes clés que les dictionnaires précédents
            new_data = {}
            for key in existing_data.keys():
                new_data[key] = existing_data[key] + data[key]

            # Enregistrer les données mises à jour dans le fichier
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False)
        else:
            print("Un participant dispose déjà de ce national id")
            return
    else:
        # Si le fichier n'existe pas, créer un nouveau fichier
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)


def save_new_tournament(file_path, data, file_path_players, start_date_timestamp, end_date_timestamp):
    """
    This function check if the file "players.txt" exist and check if the tournament does not already exist, and if
    it's ok, it create a new tournament file in .data/tournament, and rename the file "players.txt" to
    'start_date_tournament-end_date_tournament-NameTournament.txt"

    :param file_path: This is a filepath to create a new tournament file and to check if this file does not already exist.
    :param data: This json data tournament to record in .txt file.
    :param file_path_players: This is a players filepath (players.txt) to check if this file exist in ./data/players
    :param start_date_timestamp: This is a timestamp corresponding to the start date of the tournament
    :param end_date_timestamp: This is a timestamp corresponding to the end date of the tournament
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


def get_files_with_start_date_in_future(directory):
    # Récupération de la date actuelle en timestamp
    current_time = time.time()
    # Liste des fichiers dont la date de début est à venir
    future_files = []
    # Parcours des fichiers dans le répertoire donné
    for filename in os.listdir(directory):
        # Récupération de la date de début du tournoi à partir du nom du fichier
        start_date = int(filename.split("-")[0])
        # Si la date de début est à venir, on ajoute le fichier à la liste
        if start_date > current_time:
            future_files.append(os.path.join(directory, filename))
    return future_files