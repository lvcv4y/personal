import matplotlib.pyplot as plt
import math

"""
Code we used in class (practical work). Most of it is not mine: I am only responsible for the two lasts functions.
"""

def dessineMaison():
    plt.plot([1, 1, 2, 2, 1], [0, 2, 2, 0, 0], "b-") # porte
    plt.plot([3, 3, 4, 4, 3], [1, 2, 2, 1, 1], "r-") # fenetre
    plt.plot([0, 0, 2.5, 5, 0, 5, 5, 0], [0, 3, 4, 3, 3, 3, 0, 0], "k-")
    plt.grid()
    plt.show()


def dessinePolygone(x: list):
    assert len(x) > 2, "manque d'argument"
    cox = []
    coy = []
    for i in x:
        assert type(i) is list and len(i) == 2, "coordonnées erronées"
        cox.append(i[0])
        coy.append(i[1])

    cox.append(cox[0])
    coy.append(coy[0])

    plt.plot(cox, coy, "k-")
    plt.grid()
    plt.show()


def schemaDeverouillage(x: list):
    assert len(x) > 1, "manque d'argument"
    for i in range(3):
        for j in range(3):
            plt.plot(i, j, "k.", ms=30)


    cox = []
    coy = []
    for i in x:
        assert type(i) is list and len(i) == 2, "coordonnées erronées"
        cox.append(i[0])
        coy.append(i[1])

    plt.plot(cox, coy, "k-", lw=10)
    plt.show()


def que_fait_elle(n):
    LX = [-4 + x / n for x in range(8*n+1)]
    LY = [math.sin(x) for x in LX]
    plt.plot(LX, LY, "r-", lw=2)
    plt.show()


def traceCourbeCosinus(a: int = -5, b: int = 5, n: int = 30):
    trace_function(math.cos, a, b, n)


def trace_function(f: callable, a: int = -5, b: int = 5, n: int = 30):
    """
    Trace a given function.
    :param f: The function you want to get the curve of.
    :type f: callable

    :param a:
    :param b: These values defines the interval of x values (x c [a ; b]).
    :type a:
    :type b: int

    :param n: Defines the precision of the representation.
    :type n: int

    :raises ValueError: the image of a value in the given interval is forbidden, or not defined (ex: 1/x with x=0).
    """
    assert b > a, "intervalle incorrecte"
    assert isinstance(f(a), (float, int)), "f(a) n'est pas un nombre"
    cox = [a + x / n for x in range((b - a) * n + 1)]
    coy = [f(x) if isinstance(f(x), (int, float)) else None for x in cox]
    if None in coy:
        raise ValueError("f({}) n'est pas un nombre".format(cox[coy.index(None)]))

    plt.plot(cox, coy, lw=2)
    plt.show()


trace_function(math.tan, a=-10, b=10, n=20)
