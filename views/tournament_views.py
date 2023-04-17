from utils import get_all_finished_tournaments
import html2text
from jinja2 import Environment, PackageLoader, select_autoescape
import os


def display_tournaments(tournaments):
    """
    Affiche les informations d'uns liste de tournois donnée en paramètre.
    """

    for i in range(len(tournaments)):
        print("***************************************************************")
        print(
            f"( {i+1} ) ==> {tournaments[i].name} "
            f"({tournaments[i].start_date} - {tournaments[i].end_date} à {tournaments[i].location}) *"
        )
        print("***************************************************************")


def display_tournaments_in_progress(tournaments):
    """
    Affiche une liste des tournois en cours.
    """

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


def display_all_tournaments_finished():
    """
    Affiche tous les tournois qui ont été disputés.
    """

    tournaments = get_all_finished_tournaments()
    if tournaments:
        # Parcourir les informations des joueurs triées et afficher les informations de chaque joueur
        tournaments_data = []
        for tournament in tournaments:
            name_tournament = tournament.name
            start_date_tournament = tournament.start_date
            end_date_tournament = tournament.end_date
            location_tournament = tournament.location

            tournament_data = {
                'name_tournament': name_tournament,
                'start_date_tournament': start_date_tournament,
                'end_date_tournament': end_date_tournament,
                'location_tournament': location_tournament
            }
            tournaments_data.append(tournament_data)
        # Configurer l'environnement de modèle Jinja2
        env = Environment(
            loader=PackageLoader('data', 'templates'),
            autoescape=select_autoescape(['html'])
        )

        # On défini le path jusqu'aux fichiers players :
        path_tournaments_html = os.path.join('data', 'templates', 'tournaments.html')

        # Créer le fichier players.html dans le dossier templates
        with open(path_tournaments_html, 'w') as f:
            template = env.from_string('''<h1>Liste des tournois finis</h1>
                        <table>
                            <thead>
                                <tr>
                                    <th>Nom du tournoi</th>
                                    <th>Date de début du tournoi</th>
                                    <th>Date de fin du tournoi</th>
                                    <th>Lieu du tournoi</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for tournament in tournaments %}
                                    <tr>
                                        <td>{{ tournament.name_tournament }}</td>
                                        <td>{{ tournament.start_date_tournament }}</td>
                                        <td>{{ tournament.end_date_tournament }}</td>
                                        <td>{{ tournament.location_tournament }}</td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>''')
            output = template.render(tournaments=tournaments_data)
            f.write(output)

        # Affichage du html en dans la console
        with open(path_tournaments_html, 'r') as f:
            html = f.read()
            text = html2text.html2text(html)
            print(text)

    else:
        print("")
        print("         ------------------------------")
        print("         |    Aucun tournoi fini       |")
        print("         ------------------------------")
        print("")

    while True:
        keyboard = input("Appuyez sur une touche du clavier pour revenir au menu principal")
        if keyboard == "" or " ":
            break
        else:
            break
