import os
import html2text
from utils import get_all_players, get_all_finished_tournaments, get_selected_tournament
from jinja2 import Environment, PackageLoader, select_autoescape


def display_players(players):
    """
    Affiche en console les informations d'une liste de joueurs donnée en paramètre.
    """

    if len(players) > 1:
        print(f"---- ( {len(players)} participants) ----")
    else:
        print(f"---- ( {len(players)} participant) ----")
    for player in players:
        print(f"* {player.first_name} {player.last_name} ({player.national_id})")
    print("")


def display_all_players():
    """
    Affiche tous les joueurs ayant participé à au moins un tournoi.
    """

    sorted_players_info = get_all_players()
    # Initialiser un ensemble vide pour stocker les national_id déjà affichés
    displayed_ids = set()

    # Parcourir les informations des joueurs triées et afficher les informations de chaque joueur
    players_data = []
    for player in sorted_players_info:
        national_id = player['national_id']
        if national_id not in displayed_ids:
            displayed_ids.add(national_id)
            player_data = {
                'first_name': player['first_name'],
                'last_name': player['last_name'],
                'date_of_birth': player['date_of_birth'],
                'national_id': national_id
            }
            players_data.append(player_data)

    # Configurer l'environnement de modèle Jinja2
    env = Environment(
        loader=PackageLoader('data', 'templates'),
        autoescape=select_autoescape(['html'])
    )

    # On défini le path jusqu'aux fichiers players :
    path_players_html = os.path.join('data', 'templates', 'players.html')

    # Créer le fichier players.html dans le dossier templates
    with open(path_players_html, 'w') as f:
        template = env.from_string('''<h1>Liste des joueurs</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Prénom</th>
                            <th>Nom</th>
                            <th>Date de naissance</th>
                            <th>Identifiant national</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for player in players %}
                            <tr>
                                <td>{{ player.first_name }}</td>
                                <td>{{ player.last_name }}</td>
                                <td>{{ player.date_of_birth }}</td>
                                <td>{{ player.national_id }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>''')
        output = template.render(players=players_data)
        f.write(output)

    # Affichage du html en dans la console
    with open(path_players_html, 'r') as f:
        html = f.read()
        text = html2text.html2text(html)
        print(text)
    while True:
        keyboard = input("Appuyez sur une touche du clavier pour revenir au menu principal")
        if keyboard == "" or " ":
            break
        else:
            break


def display_all_players_in_tournament(display_tournaments_fn):
    """
    Affiche tous les joueurs d'un tournoi donné.
    """

    tournaments = get_all_finished_tournaments()
    display_tournaments_fn(tournaments)
    selected_tournament = get_selected_tournament(tournaments)

    player_dict_list = []
    for player in selected_tournament.players:
        player_dict = {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "date_of_birth": player.date_of_birth,
            "national_id": player.national_id
        }
        player_dict_list.append(player_dict)

    if not selected_tournament:
        print("Vous n'avez encore aucun tournoi fini pour le moment")
    else:
        # Trier la liste players_info par ordre alphabétique
        sorted_players_info = sorted(player_dict_list, key=lambda x: x['last_name'])

        # Parcourir les informations des joueurs triées et afficher les informations de chaque joueur
        players_data = []
        for player in sorted_players_info:
            player_data = {
                'tournament_name': selected_tournament.name,
                'first_name': player['first_name'],
                'last_name': player['last_name'],
                'date_of_birth': player['date_of_birth'],
                'national_id': player['national_id']
            }
            players_data.append(player_data)

        # Configurer l'environnement de modèle Jinja2
        env = Environment(
            loader=PackageLoader('data', 'templates'),
            autoescape=select_autoescape(['html'])
        )

        # On défini le path jusqu'aux fichiers players :
        path_players_html = os.path.join('data', 'templates', 'players_in_tournament.html')

        # Créer le fichier players.html dans le dossier templates
        with open(path_players_html, 'w') as f:
            template = env.from_string('''<h1>Liste des joueurs</h1>
                    <table>
                        <thead>
                            <tr>
                                <th>Nom du tournoi</th>
                                <th>Prénom</th>
                                <th>Nom</th>
                                <th>Date de naissance</th>
                                <th>Identifiant national</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for player in players %}
                                <tr>
                                    <td>{{ player.tournament_name }}</td>
                                    <td>{{ player.first_name }}</td>
                                    <td>{{ player.last_name }}</td>
                                    <td>{{ player.date_of_birth }}</td>
                                    <td>{{ player.national_id }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>''')
            output = template.render(players=players_data)
            f.write(output)

        # Affichage du html en dans la console
        with open(path_players_html, 'r') as f:
            html = f.read()
            text = html2text.html2text(html)
            print(text)
        while True:
            keyboard = input("Appuyez sur une touche du clavier pour revenir au menu principal")
            if keyboard == "" or " ":
                break
            else:
                break
