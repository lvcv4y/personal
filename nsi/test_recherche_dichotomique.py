from random import randint

"""
Custom testing setup for searching algorithm (see recherche_dichotomique.py)
"""


class BadIndexReturnedError(Exception):
    """
    Exception with custom message, for easier logging purposes.
    """

    def __init__(self, test_id: int, used_list: list, awaited_index: int, received_index: int):
        self.message = "Le test n°{} s'est mal passé :( \n Le résultat attendu était " \
                       "\"{}\" (ce qui correspond a l'index de la valeur '{}' dans la liste '{}'), " \
                       "mais \"{}\" a été recu".format(test_id, awaited_index, used_list[awaited_index], used_list,
                                                       received_index)
        super(self).__init__(self.message)


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


def search_test(search_function: callable, n: int = 10000, valid_log: bool = True):
    """
    Automatically tests a searching function.

    :param search_function: the searching function to test.
    :type search_function: callable

    :param n: the number of tests you want to be done.
    :type n: int

    :param valid_log: Defines if a message should be printed when a test is successfully passed.
    :type valid_log: bool

    :raises BadIndexReturnedError: When a test is not passed.
    """
    for i in range(n):
        rand_list = sorted(get_random_list())

        rand_index = randint(0, len(rand_list) - 1)

        testing_index = search_function(rand_list, rand_list[rand_index])

        if testing_index != rand_index:
            print("Liste : {}\nObjet : {}".format(rand_list, rand_list[rand_index]))
            raise BadIndexReturnedError(i + 1, rand_list, rand_index, testing_index)

        if valid_log:
            print("Test n°{} passé !".format(i + 1))

    print("L'ensemble des {} tests ont été passés avec succès !".format(n))
