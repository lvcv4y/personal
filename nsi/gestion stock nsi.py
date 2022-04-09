from enum import Enum

"""
Exercise I've done in info class last year. Variable, comments, functions' name and classes are in french.
The code is quite poorly documented, but I have lost the exercise instructions. The code is still explicit enough
for a french speaker though.
"""

"""
TODO
savoir si une commande est réalisable : DONE
connaitre réapprovisionnement necessaire pour realise une commande actuellement non realisable : DONE
mettre a jour le stock a partir dune commande realisable : DONE
rajouter un nouveau type de lampe au catalogue, ainsi que le protocole de fabrication associé : DONE
"""


class Pieces(Enum):
    """
    utilisation d'une enumeration pour les differents types de pieces
    (l'utilisation de constantes réduit les potentielles erreurs (faute de frappe,...))
    """
    LED = 1
    HALOGENE = 2
    DOUILLE_SIMPLE = 3
    INTERRUPTEUR = 4
    GRADATEUR = 5


stock = {
    Pieces.LED: 2,
    Pieces.HALOGENE: 0,
    Pieces.DOUILLE_SIMPLE: 2,
    Pieces.INTERRUPTEUR: 1,
    Pieces.GRADATEUR: 0
}

catalogue = {
    "L1": {Pieces.LED: 2, Pieces.DOUILLE_SIMPLE: 2, Pieces.INTERRUPTEUR: 1},
    "L2": {Pieces.HALOGENE: 4, Pieces.DOUILLE_SIMPLE: 2, Pieces.GRADATEUR: 2},
    "L3": {Pieces.LED: 3, Pieces.HALOGENE: 2, Pieces.DOUILLE_SIMPLE: 2, Pieces.INTERRUPTEUR: 1}
}

commandes = [
    # {"type_lampe" : nombre}
    # ex : {"L1": 3}
]

livraisons = [
    # {"type_pieces": nombre livré}
    # ex : {"led" : 1}
]


def livraison(pieces_livrees: dict):
    pieces_valides = set(item.value for item in Pieces)

    for piece, nombre in pieces_livrees.items():
        if piece.value in pieces_valides:
            stock[piece] += nombre
        else:
            print("piece inconnue recue (code {})".format(piece))

    livraisons.append(pieces_livrees)


def count_realisable(type_lampe: str):
    return min(
        [v // catalogue[type_lampe][piece] for piece, v in stock.items() if piece in catalogue[type_lampe].keys()]
    )


def get_piece_from_command(commande: dict) -> dict:
    pieces_demandees = {}
    for k, v in commande.items():
        pieces_demandees.update({piece: nombre * v for piece, nombre in catalogue[k].items()})

    return pieces_demandees


def is_command_realisable(commande: dict) -> bool:
    pieces_demandees = get_piece_from_command(commande)

    for piece, nombre in pieces_demandees.items():
        if stock[piece] < nombre:
            return False

    return True


def reapprovisionnement(commande: dict) -> dict:
    pieces = get_piece_from_command(commande)
    for piece, nombre in pieces.items():
        if stock[piece] < nombre:
            pieces[piece] = nombre - stock[piece]

    return pieces


def realize_commande(commande: dict):
    assert is_command_realisable(commande), "La commande n'est pas realisable"
    pieces = get_piece_from_command(commande)

    for piece, nombre in pieces.items():
        stock[piece] -= nombre

    commandes.append(commande)  # ajout historique des commandes (ptit cadeau pour la gestion)


def add_new_lampe(name: str, pieces: dict):
    for k, v in pieces.items():
        if type(k) is not Pieces:
            raise TypeError("{} n'est pas une piece valide".format(k))

    catalogue[name] = pieces
