from utils import input_validation, file_manager
from models import Player
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
        again_or_no = input("Voulez-vous ajouter un autre participant ? ('q' pour quitter) ")
        if str(again_or_no) == 'q':
            break
        elif again_or_no == '':
            add_player_to_database()
