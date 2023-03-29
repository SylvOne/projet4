import json
import os



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


def save_tournament(file_path, data):
    # Vérifier si le fichier existe
    if os.path.isfile(file_path):
        pass
        """     # Si le fichier existe, ouvrir le fichier en mode lecture
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
            return"""
    else:
        # Si le fichier n'existe pas, créer un nouveau fichier
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
