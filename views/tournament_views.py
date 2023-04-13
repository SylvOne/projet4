from views import player_views


def display_tournaments(tournaments):
    for i in range(len(tournaments)):
        print("***************************************************************")
        print(f"( {i+1} ) ==> {tournaments[i].name} ({tournaments[i].start_date} - {tournaments[i].end_date} à {tournaments[i].location}) *")
        print("***************************************************************")
        player_views.display_players(tournaments[i].players)


def display_tournaments_in_progress(tournaments):
    if tournaments:
        print("")
        print("         ------------------------------")
        print("         | Liste des tournois en cours |")
        print("         ------------------------------")
        print("")
        display_tournaments(tournaments)
    else:
        print("")
        print("         ------------------------------")
        print("         |    Aucun tournoi en cours   |")
        print("         ------------------------------")
        print("")