from unidecode import unidecode
import string


def rm_accent_punct_space(str):
    """
    Supprime les accents, la ponctuation et les espaces de la chaîne de caractères 's'.
    """
    # Supprimer la ponctuation
    s = str.translate(str.maketrans("", "", string.punctuation))

    # Supprimer les accents
    s = unidecode(s)

    # Mettre la première lettre de chaque mot en majuscule tout en supprimant les espaces
    s = "".join([word.capitalize() for word in s.split()])

    return s
