# Centre Échecs

## Introduction
Le Centre Échecs est un programme autonome et hors ligne qui permet de gérer des tournois d'échecs. 
Le programme est écrit en Python et lancé depuis la console. L'exécution du programme doit ressembler à ceci :
`python main.py`. Le programme fonctionne sous Windows, Mac ou Linux et a un fichier `requirements.txt` 
listant les dépendances nécessaires à son exécution.

## Installation
1. Clonez le dépôt avec `git clone https://github.com/SylvOne/projet4.git`.
2. Naviguez jusqu'au dossier du programme avec `cd projet4`.
3. Créez un dossier `data` et dans ce dossier créez suivants:
 - `data/players`
 - `data/templates`
 - `data/tournaments`
4. Créez un environnement virtuel avec `python -m venv venv` sur Windows ou `python3 -m venv venv` sur Linux/Mac
5. Activez l'environnement virtuel avec `source venv/bin/activate` 
sur Linux/Mac ou `.\venv\scripts\activate` sur Windows.
6. Installez les dépendances avec `pip install -r requirements.txt`.

## Utilisation
- Lancez le programme avec `python main.py`. 
- Suivez les instructions à l'écran :<br>
`1. Ajouter des participants pour un futur tournoi`<br>
`2. Ajouter des participants à un tournoi existant`<br>
`3. Créer un tournoi`<br>
`4. Lancer un tournoi`<br>
`5. Voir tous les joueurs qui ont participé à un tournoi`<br>
`6. Voir tous les tournois disputés`<br>
`7. Voir tous les joueurs d'un tournoi`<br>
`8. Voir tous les tours d'un tournoi et tous les matchs du tour `<br>


## Rapport Flake8-HTML
1. Soyez sûr d'avoir installé Flake8 et flake8-html avec `pip install flake8` et `pip install flake8-html`
2. Générez un rapport Flake8-HTML avec 
`flake8 --exclude=.git,__pycache__,venv --max-line-length=119 --format=html --htmldir=flake8_rapport`.
3. Ouvrez le fichier `flake8_rapport/index.html` pour voir le rapport.

**Note :** Assurez-vous de conserver les fichiers JSON dans le dossier `data` 
pour sauvegarder les données du programme. 
Ne supprimez pas ces fichiers si vous voulez conserver l'historique des tournois et des joueurs.

**Bon tournoi !**
