import matplotlib.pyplot as plt


def trace(f: int = None, o_a: int = None, a_b: int = None):
    """
    Make and show a drawing of the image of an object AB through a converging lens.
    Note: it supports virtual images.
    :param f: Focal distance of the lens.
    :param o_a: Distance between the lens and the object.
    :param a_b: Height of the object.
    """
    oa_prime = 1 / (1 / f + 1 / o_a)

    # coefficient of the straight line that goes through the O point
    coefficient_o_line = a_b / o_a

    # coefficient of the straight line (B; F)
    coefficient_f_b = a_b / (o_a + f)

    """(-f, 0)
       (oa, a_b)

       0 = a_b / (-f - oa)x + k
       """

    k_2 = -coefficient_f_b * -f
    x = (k_2 * o_a) / a_b

    plt.scatter(0, 0, marker=".")
    plt.annotate("O", (0, 0))

    plt.scatter(o_a, 0)
    plt.annotate("A", (o_a, 0))

    plt.scatter(o_a, a_b)
    plt.annotate("B", (o_a, a_b))

    plt.scatter(x, 0)
    plt.annotate("A'", (x, 0))

    plt.scatter(x, k_2)
    plt.annotate("B'", (x, k_2))

    plt.scatter(-f, 0)
    plt.annotate("F", (-f, 0))

    plt.scatter(f, 0)
    plt.annotate("F'", (f, 0))

    x_lim = plt.gca().get_xlim()

    plt.plot([o_a, 0], [i * coefficient_f_b + k_2 for i in [o_a, 0]], "b-")
    plt.plot([0, x_lim[1]], [k_2]*2, "b-")

    if abs(o_a) < f:  # if we have a virtual image
        plt.plot([x_lim[0], o_a], [coefficient_f_b * x_lim[0] + k_2, a_b], "b-")
        plt.plot([x_lim[0], 0], [k_2] * 2, "b-.")

    plt.plot(x_lim, [i * coefficient_o_line for i in x_lim], "r-")

    plt.plot([x_lim[0], 0], [a_b] * 2, "g-")

    # using calculus, we can deduce that the line that goes (0; a_b) to F' has the following equation :
    # f(x) = (a_b/-f)*x + a_b
    plt.plot([0, x_lim[1]], [a_b, (a_b/-f)*x_lim[1] + a_b], "g-")

    if abs(o_a) < f:  # if we have a virtual image
        plt.plot([x_lim[0], 0], [(a_b/-f)*x_lim[0] + a_b, a_b], "g-.")

    # objects
    plt.plot([o_a, o_a], [0, a_b], "k-")
    plt.plot([oa_prime, oa_prime], [0, k_2], "k-" if abs(o_a) >= f else "k-.")

    # TODO arrows at edges

    plt.plot(plt.gca().get_xlim(), [0] * 2, "k-")
    plt.plot([0] * 2, plt.gca().get_ylim(), "k-")
    plt.grid()
    plt.show()


trace(f=5, o_a=-10, a_b=5)
