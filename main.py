from controllers import player_controller, tournament_controller
from views import (display_all_players, display_all_tournaments_finished,
                   display_all_players_in_tournament, display_tournaments,
                   display_all_rounds_tournament)


def main_menu():
    print("Menu principal")
    print("1. Ajouter des participants pour un futur tournoi")
    print("2. Ajouter des participants à un tournoi existant")
    print("3. Créer un tournoi")
    print("4. Lancer un tournoi")
    print("5. Voir tous les joueurs qui ont participé à un tournoi")
    print("6. Voir tous les tournois disputés")
    print("7. Voir tous les joueurs d'un tournoi")
    print("8. Voir tous les tours d'un tournoi et tous les matchs du tour")
    print("9. Quitter")

    choice = input("Entrez votre choix (1, 2, 3, 4, 5, 6, 7, 8 ou 9) : ")

    if choice == "1":
        player_controller.add_player_to_database()
    elif choice == "2":
        player_controller.add_players_tournament()
    elif choice == "3":
        tournament_controller.create_tournament()
    elif choice == "4":
        tournament_controller.start_round_tournament()
    elif choice == "5":
        display_all_players()
    elif choice == "6":
        display_all_tournaments_finished()
    elif choice == "7":
        display_all_players_in_tournament(display_tournaments)
    elif choice == "8":
        display_all_rounds_tournament(display_tournaments)
    elif choice == "9":
        print("Au revoir !")
        exit()
    else:
        print("Choix invalide. Veuillez entrer 1, 2, 3, 4, 5, 6 ou 7")
        main_menu()


if __name__ == "__main__":
    while True:
        main_menu()
