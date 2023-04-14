import os
import html2text
from utils import (
    get_all_finished_tournaments, get_selected_tournament,
    get_tournament_data, get_top_players, write_html
)


def display_all_rounds_tournament(display_tournaments_fn):
    tournaments = get_all_finished_tournaments()
    display_tournaments_fn(tournaments)
    selected_tournament = get_selected_tournament(tournaments)

    if selected_tournament:
        tournaments_data = get_tournament_data(selected_tournament)
        top_players = get_top_players(selected_tournament)
        write_html(selected_tournament, tournaments_data, top_players)
        path_tournaments_html = os.path.join('data', 'templates', 'tournament_rounds_and_players.html')
        with open(path_tournaments_html, 'r') as f:
            html = f.read()
            text = html2text.html2text(html)
            print(text)
            while True:
                keyboard = input("Appuyez sur une touche du clavier pour revenir au menu principal")
                if keyboard == "" or " ":
                    break
                else:
                    break
    else:
        print("Il n'y a aucun tournoi fini")
        while True:
            keyboard = input("Appuyez sur une touche du clavier pour revenir au menu principal")
            if keyboard == "" or " ":
                break
            else:
                break
