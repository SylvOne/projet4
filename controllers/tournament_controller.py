from models import Tournament, Player
from utils import load_players_to_json, save_new_tournament, is_valid_start_date_tournament, is_valid_end_date_tournament, rm_accent_punct_space
import os
from datetime import datetime


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

    # charger les joueurs pour la création d'un tournoi
    path_players = os.path.join('data', 'players', 'players.txt')
    players_json = load_players_to_json(path_players)
    tournament = Tournament(name, location, start_date, end_date, num_rounds, description)

    for i in range(len(players_json['last_name'])):
        last_name = players_json['last_name'][i]
        first_name = players_json['first_name'][i]
        birth_date = players_json['date_of_birth'][i]
        national_id = players_json['national_id'][i]
        player = Player(last_name, first_name, birth_date, national_id)
        tournament.add_player(player)

    # Save tournament to json in ./data/tournaments
    tournament_file_name = str(int(datetime.strptime(tournament.start_date, '%d/%m/%Y').timestamp()))+"-"+str(int(datetime.strptime(tournament.end_date, '%d/%m/%Y').timestamp()))+"-"+rm_accent_punct_space(tournament.name)+".txt"
    path_tournament = os.path.join('data', 'tournaments', tournament_file_name)
    data_tournament = tournament.export_data_tournament()
    players_to_json = []
    for player in data_tournament['players']:
        players_to_json.append(player.export_data_player())
    # Création du nouveau dictionnaire avec les mêmes clés que les dictionnaires précédents
    data_tournament_to_json = {}
    for key in data_tournament.keys():
        if key == "players":
            data_tournament_to_json[key] = players_to_json
        else:
            data_tournament_to_json[key] = data_tournament[key]
    save_new_tournament(path_tournament, data_tournament_to_json, path_players, str(int(datetime.strptime(tournament.start_date, '%d/%m/%Y').timestamp())), str(int(datetime.strptime(tournament.end_date, '%d/%m/%Y').timestamp())))
