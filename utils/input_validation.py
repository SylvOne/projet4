import re
from datetime import datetime, timedelta


def is_valid_national_id(national_id):
    """
    Permet de s'assurer que le national id est valide.
    """

    pattern = re.compile(r"^[A-Za-z]{2}\d{5}$")
    return bool(pattern.match(national_id))


def is_valid_date(date_string):
    """
    Permet de s'assurer que le format de la date entrée par l'utilisateur est valide.
    """

    try:
        day, month, year = map(int, date_string.split('/'))
        return 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 9999
    except ValueError:
        return False


def is_valid_start_date_tournament(start_date):
    """
    Permet de s'assurer que la date de début d'un tournoi est actuelle ou future.
    """

    try:
        start_date_obj = datetime.strptime(start_date, '%d/%m/%Y').date()
        if start_date_obj >= datetime.now().date():
            return True
        else:
            print("La date de début doit être une date future ou actuelle.")
            return False
    except ValueError:
        print("La date de début n'est pas au format JJ/MM/AAAA.")


def is_valid_end_date_tournament(end_date, start_date_obj):
    """
    Permet de s'assurer que la date de fin d'un tournoi est ultérieure à la date de début du tournoi
    """

    try:
        end_date_obj = datetime.strptime(end_date, '%d/%m/%Y')
        if end_date_obj < start_date_obj + timedelta(days=1):
            print("La date de fin doit être au moins un jour après la date de début.")
        else:
            return True
    except ValueError:
        print("La date de fin n'est pas au format JJ/MM/AAAA.")
