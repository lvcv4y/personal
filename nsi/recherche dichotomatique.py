from test_recherche_dichotomique import search_test

"""
Dichotomous search algorithm.
"""


def recherche_dichotomique(tab: list, val):
    """
    Dichotomous search algorithm.

    :param tab: The list you want to search in.
    :type tab: list

    :param val: The value you want the index of.

    :return: The index of the given value in the given list.
    :rtype: int
    """
    assert len(tab) > 0 and val in tab, "Le tableau donné doit etre non vide et contenir la valeur"
    debut = 0
    fin = len(tab)
    count = 0
    m = -1

    while debut < fin:
        m = (debut+fin)//2
        count += 1

        if tab[m] == val:
            break

        if tab[m] > val:
            fin = m
        else:
            debut = m

    return m

# search_test(recherche_dichotomique, 10, False)
