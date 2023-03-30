from controllers import player_controller, tournament_controller

def main_menu():
    print("Menu principal")
    print("1. Ajouter des participants pour un futur tournoi")
    print("2. Ajouter des participants à un tournoi existant")
    print("3. Créer un tournoi")
    print("4. Quitter")

    choice = input("Entrez votre choix (1, 2 ou 3) : ")

    if choice == "1":
        player_controller.add_player_to_database()
    elif choice == "2":
        player_controller.add_players_tournament()
    elif choice == "3":
        tournament_controller.create_tournament()
    elif choice == "4":
        print("Au revoir !")
        exit()
    else:
        print("Choix invalide. Veuillez entrer 1, 2 ou 3.")
        main_menu()

if __name__ == "__main__":
    while True:
        main_menu()
