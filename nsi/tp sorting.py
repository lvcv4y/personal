from random import randint

"""
Sorting algorithm implementations we had to do in class.
"""


class SortingTestNotPassedError(Exception):
    def __init__(self, test_id: int, awaited_result: list, received_result: list):
        self.message = "Le test n°{} s'est mal passé :( \n Le résultat attendu était " \
                       "\"{}\" (ce qui correspond a une liste triée correctement), mais \"{}\" a été recu" \
            .format(test_id, awaited_result, received_result)
        super(self).__init__(self.message)


def trier(tab: list):
    """
    Selection sort implementation.
    :param tab: the list to sort.
    :return: the sorted list.
    """
    for i in range(len(tab) - 1):
        mini = i

        for j in range(i + 1, len(tab)):
            if tab[j] < tab[mini]:
                mini = j

        if tab[mini] < tab[i]:
            temp = tab[i]
            tab[i] = tab[mini]
            tab[mini] = temp

    return tab


def tri_insertion(tab: list):
    """
    Insertion sort implementation.
    :param tab: the list to sort.
    :return: the sorted list.
    """
    for i in range(1, len(tab)):
        val = tab[i]
        j = i
        while j > 0 and tab[j - 1] > val:
            tab[j] = tab[j - 1]
            j -= 1

        tab[j] = val

    return tab


def get_random_list(start_len=1, end_len=20, start_val=0, end_val=100, unique_obj=True):
    """
    Generate a customizable random list. Use for debug purposes.

    :type start_len:
    :type start_len: int

    :param start_len:
    :param end_len: These values defines the interval in which the length of the generated list will be picked.


    :type start_len:
    :type start_len: int

    :param start_val:
    :param end_val: These values defines the interval in which the values of the generated list will be picked.

    :param unique_obj: Defines if the list can contain duplicate numbers.
    :type unique_obj: bool

    :return: The generated list.
    :rtype: list
    """

    res = []
    for _ in range(randint(start_len, end_len)):

        new_val = randint(start_val, end_val)

        if unique_obj:
            while new_val in res:
                new_val = randint(start_val, end_val)

        res.append(new_val)

    return res


def sorting_test(sorting_function: callable, n: int = 100, valid_log: bool = True):
    """
    Automatically tests a sorting function.

    :param sorting_function: the sorting function to test.
    :type sorting_function: callable

    :param n: the number of tests you want to be done.
    :type n: int

    :param valid_log: Defines if a message should be printed when a test is successfully passed.
    :type valid_log: bool

    :raises SortingTestNotPassedError: When a test is not passed.
    """
    for i in range(n):
        rand_list = get_random_list()
        testing_sort = sorting_function(rand_list)
        correctly_sorted = sorted(rand_list)

        if testing_sort != correctly_sorted:
            # releve une erreur si la liste triee par la fonction à tester
            # est différente de la liste triée correctement
            raise SortingTestNotPassedError(i + 1, correctly_sorted, testing_sort)

        if valid_log:
            print("test #{} OK".format(i))

    print("L'ensemble des {} tests ont été passés avec succès".format(n))


sorting_test(tri_insertion, 100000, False)
