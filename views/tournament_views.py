from views import player_views

def display_tournaments(tournaments):
    for i in range(len(tournaments)):
        print("***************************************************************")
        print(f"( {i+1} ) ==> {tournaments[i].name} ({tournaments[i].start_date} - {tournaments[i].end_date} à {tournaments[i].location}) *")
        print("***************************************************************")
        player_views.display_players(tournaments[i].players)