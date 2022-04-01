def euclid_division(a: int, b: int) -> tuple:
    """get the euclid divisions of a by b. Note : this function only works with positive integers
    :param a: the integer that you want to get the euclid's division form from (strictly positive)
    :type a: int

    :param b: the integer that you want to divide "a" with (strictly positive)
    :type b: int

    :returns: if a = qb+r (b and r both positive integers and 0 <= r < b), returns a tuple as follow : (a, q, b, r)
    :rtype: tuple
    """
    assert type(a) is int is type(b), "Arguments are not both integers"
    assert a > 0 and b > 0, "Arguments are not both strictly positive"
    return a, a // b, b, a % b  # a = q*b + r


def euclid_algorithm(a: int, b: int, explicit: bool = True) -> tuple:
    """apply the euclid algorithm to get a couple of solutions to the equation au+bv = gcd(a ; b) (u and v being
    integers).
    Note: this function only works with positive integers.

    :param a: an strictly positive integer (see the equation in the function description)
    :type a: int

    :param b: an strictly positive integer (see the equation in the function description)
    :type b: int

    :param explicit: Indicate if you want a detailed printed output of the different steps of the algorithm
    :type explicit: bool

    :returns: returns a tuple (u, a, v, b) being a solution to the equation au+bv = gcd(a; b)
    :rtype: tuple
    """

    assert type(a) is int is type(b), "Passed arguments a and b are not both integers"
    assert a > 0 and b > 0, "Passed arguments a and b are not both strictly positive integers"

    # retrieving the gcd using the euclid method
    # we are using the fact that if a = bq+r, gcd(a; b) = gcd(b; r) to "simplify" until
    # b is a multiple of r (the last value of r that differs from 0 is the gcd)

    if a > b:
        divisions = [euclid_division(a, b)]
    else:
        divisions = [euclid_division(b, a)]

    while divisions[-1][3] != 0:

        # "simplifying" and keeping track of every euclid's divisions we've made

        last = divisions[-1]
        divisions.append(euclid_division(last[2], last[3]))

    if len(divisions) <= 1:

        if explicit:
            print("{} = {}*{} + 0".format(divisions[0][0], divisions[0][1], divisions[0][2]))
            print("this means that, in that specific case, a is a multiple of b (or vice versa)")

        # a is a multiple of b (or b is a multiple of a) (a = qb ; or b = qa)
        if a > b:

            # a is a multiple of b ; a = qb and au + bv = b is the equation ; because b is the gcd
            # so, we have (qb)u + bv = b, is which simplifiable by b : qu + v = 1
            # thus, we have a generic form of v : v = 1 - q*u ; which works for every values of u
            # to simplify, we use u=1, which leads to v = 1-q
            # so we returns (1, a, 1-q, b) as a + (1-q)b = b, as proven above

            if explicit:
                print("General solution when a = bq : v = 1-qu ; u an integer")
                print("Example with u=1 for the equation {}u + {}v = {} : ".format(a, b, b))
                print("u = 1 ; v = {}".format(1-divisions[0][1]))

            return 1, a, 1-divisions[0][1], b
        else:
            # same thing, but reversed : b = qa
            if explicit:
                print("General solution when b = ba : u = 1-qv ; v an integer")
                print("Example with v=1 for the equation {}u + {}v = {} : ".format(a, b, a))
                print("u = {} ; v = 1".format(1-divisions[0][1]))

            return 1 - divisions[0][1], a, 1, b

    divisions.pop()  # we don't need the last division, as it is b = gcd(a; b)*q + 0, and q is here useless

    # Now that we have every euclid's divisions until the gcd,
    # we "rotate" the equations to get them from c = dq+r (c and d integers)
    # to r = c - dq

    equations = [
        # r : (a, q, b) <=> r = a - q*b
        (el[3], el[0], -el[1], el[2])  # tuple because it doesn't need to be mutable
        for el in divisions
    ]

    if explicit:
        for i in range(len(divisions)):

            # explains the "rotation" we've made

            div = divisions[i]
            print("{} = {}*{} + {} <=> {} = {} - {}*{}".format(
                div[0], div[1], div[2], div[3], div[3], div[0], div[1], div[2]
            ))

    # q1, a1, q2, a2 <=> gcd = q1*a1 + q2*a2

    solutions = list(equations[-1])
    solutions[0] = 1

    # this is where the real algorithm takes place :
    # we have, in the "solutions" variable, 4 values as follow : (u, c, v, d)
    # this variable is in fact representing the follow equation : uc+vd
    # which is equals the gcd(a; b). How can we be sure though ?
    # well, because we popped out gcd(a ; b) = qx + 0 (x integer) from divisions;
    # equations[-1]is gcd(a; b) = c + v*d (gcd value is replaced by 1, because 1*c-v*d = gcd(a; b))
    #
    # However, because we used the fact that gcd(a; b) = gcd(b; r) (if a = qb+r)
    # and that we kept track of every divisions we have made,
    # equations[-2] is telling us that d = e - n*c (e and n positive integers)
    # that way, we can replace our previous equations by
    # gcd(a; b) = c + v(e - n*c) = c + ve - vnc = (1-vn)c + ve
    # However, we can also decompose c as a combination of e and another integer using equations[-2]
    # And so on and so forth, until we get u*a + v*b = gcd(a; b)

    start = equations.pop()  # equations[-1] is stored for output purposes
    equations.reverse()  # we reverse the list to make the for-loop easier

    if explicit:
        print("*"*10)
        print("{} = {} - {}*{}".format(start[0], start[1], abs(start[2]), start[3]))

    for i, eq in enumerate(equations):

        # solutions is storing the following equation : u*c + v*d (= gcd(a; b))
        # We always replace either the first or the second side in the same order :
        # first the second one, then the first, then the second,...

        # "eq" is storing an equation as follow : x = e - n*y;
        # x and y being either c or d

        if i % 2:

            if explicit:
                print("*****")

                print("{} = {}*({} - {}*{}) {} {}*{}".format(
                    start[0], solutions[0], eq[1], abs(eq[2]), eq[3], "+" if solutions[2] > 0 else "-",
                    abs(solutions[2]), solutions[3]
                ))

                print("{} = {}*{} {} {}*{} {} {}*{}".format(
                    start[0], solutions[0], eq[1], "+" if solutions[0] * eq[2] * eq[3] > 0 else "-",
                    abs(solutions[0] * eq[2]), eq[3], "+" if solutions[2] > 0 else "-", abs(solutions[2]), solutions[3]
                ))

            # if c = e - nd

            # uc + vd = u(e - nd) + vd = ue - und + vd = ue + (v - un)d
            # the new value of solutions[2] (== v) is v - un, u stored in solutions[0]
            # and -n stored in eq[2] (this is why we are using "+=" instead of "-=")
            solutions[2] += (eq[2] * solutions[0])

            # the new value of "c" is now "e", so eq[1]
            solutions[1] = eq[1]

        else:

            if explicit:
                print("*****")
                print("{} = {}*{} {} {}*({} - {}*{})".format(
                    start[0], solutions[0], solutions[1], "+" if solutions[2] > 0 else "-",
                    abs(solutions[2]), eq[1], abs(eq[2]), eq[3]
                ))
                print("{} = {}*{} {} {}*{} {} {}*{}".format(
                    start[0], solutions[0], solutions[1], "+" if solutions[2] * eq[1] > 0 else "-",
                    abs(solutions[2]), abs(eq[1]), "+" if solutions[2] * eq[2] * eq[3] > 0 else "-",
                    solutions[2] * eq[2], eq[3]
                ))

            # same as the other case (see above if block)
            # but this time we have d = e - nc

            solutions[0] += (eq[2] * solutions[2])
            solutions[3] = eq[1]

        if explicit:
            print("{} = {}*{} {} {}*{}".format(
                start[0], solutions[0], solutions[1], "+" if solutions[2] * solutions[3] > 0 else "-",
                abs(solutions[2]), abs(solutions[3])
            ))

    if explicit:
        print("*"*10)
        print("Couple of solution (u; v) found for the equation {}*u + {}*v = {} : "
              .format(solutions[1], solutions[3], start[0]))
        print("u = {} ; v = {}".format(solutions[0], solutions[2]))

    return tuple(solutions)  # returns a tuple instead of a list, as the output should not be mutable
