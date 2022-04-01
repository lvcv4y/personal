from fractions import Fraction
from random import randint


class MatrixRow:
    """
    A class representing a row of a Matrix. Should not be used alone, as
    it is a simple list abstraction with methods to simplify AugmentedMatrix.solve() process.

    Attributes:
        inner_row: The inner list containing the value of the row. Should not be
            directly manipulated.

    Property:
        length: The inner list length.

    Methods:
        multiply_by_scalar(scalar):
            Multiply the values of the manipulated row by the given scalar.

        get_multiplied_by_scalar(scalar):
            Get a copy of the row with every value multiplied by the given scalar.

        add(row):
            Add to every item in the row its corresponding value in the passed row.
    """

    def __init__(self, row: list):
        """
        Constructor of the MatrixRow class.

        :param row: List containing the values the row should hold at first.
        :type row: list

        :raises ValueError: if the row argument contains invalid numbers.
        """

        self.inner_row = list()

        for i in row:
            try:
                self.inner_row.append(Fraction(i))
            except ValueError:
                # "i" element is not a thing that can be converted in a number
                raise ValueError("the list passed as argument contains elements"
                                 " that could not be converted into a \"Fraction\" instance"
                                 "\"{}\" is not a valid number).".format(i))

    @property
    def length(self) -> int:
        """
        Length property.
        :return: the length of the inner list.
        :rtype: int
        """
        return len(self.inner_row)

    def multiply_by_scalar(self, scalar: Fraction):
        """
        Multiply every value of the current row by the given scalar.
        Note : this DOES modify the inner list, but does NOT returns anything.

        :param scalar: the scalar you want the row to be multiplied by.
        :return: Nothing, this modifies the inner list.
        :raises ValueError: if the scalar given is not a number.
        """

        if type(scalar) not in [int, float, Fraction]:
            raise ValueError("The given scalar \"{}\" is not a valid number.".format(scalar))

        for i in range(self.length):
            self[i] *= scalar

    def get_multiplied_by_scalar(self, scalar: Fraction) -> "MatrixRow":
        """
        Get a copy of the row with every element multiplied by the given scalar.
        Note : this does NOT modify the values of this instance, but RETURNS a modified copy.

        :param scalar: the scalar you want the values of the copy to be multiplied by.
        :return: A list containing the elements of the row multiplied by the scalar.
        :rtype: MatrixRow

        :raises ValueError: if the scalar given is not a number.
        """

        if type(scalar) not in [int, float, Fraction]:
            raise ValueError("The given scalar \"{}\" is not a valid number".format(scalar))

        return MatrixRow([i*scalar for i in self.inner_row])

    def add_row(self, row: "MatrixRow"):
        """
        Add, to every element of the inner row, its corresponding element in the passed row.
        Meaning, we are adding to the nth element of the inner row, the nth value of the given row.

        :param row: The row you want to add to this one.

        :raises ValueError: the "row" passed is not an instance of Matrix row,
            or does not have the same length as the inner row :
            addition does not make any sense in that case.
        """

        if type(row) is not MatrixRow:
            raise ValueError("Given argument is not a MatrixRow instance.")

        if row.length != self.length:
            raise ValueError("Lines do not have the same length : addition has no sense.")

        for i in range(len(self.inner_row)):
            self[i] += row[i]

    def __str__(self):
        return "MatrixRow{{{}}}".format(', '.join(str(el) for el in self.inner_row))

    def __setitem__(self, key, value):
        if type(key) is not int:
            raise ValueError("The key argument should be an integer")

        try:
            self.inner_row[key] = Fraction(value)
        except ValueError:
            raise ValueError("The value given should be a number (convertible to Fraction)")

    def __getitem__(self, item) -> Fraction:
        if type(item) is not int:
            raise ValueError("The key argument should be an integer")

        return self.inner_row[item]


class AugmentedMatrix:
    """
    A class representing an augmented matrix, used to solve systems
    with n variables and with at least n equations (Gaussian elimination).
    Note : this implementation does not verify if the system passed is solvable for now.

    Attributes:
        rows_list: the matrix itself, represented as a list of its row
            (each row being a list of n elements, n the "width" of the matrix.).

    Methods:

        static - wrap(list):
            convert a 2-dimension list into an AugmentedMatrix instance.

        solve():
            manipulate the matrix to make an identity matrix appear (last column excluded, as it
            will hold the solutions).

        get_last_column():
            get the last column of the matrix, containing the solutions if the
            solve method has been called once.
    """

    @staticmethod
    def wrap(array: list) -> "AugmentedMatrix":
        """
        Convert a 2-dimension list into an AugmentedMatrix instance.
        :param array: the 2-dimensions list
        :return: the AugmentedMatrix object corresponding to the input.
        :rtype: AugmentedMatrix

        :raises ValueError: some values in one of the list is incorrect (wrong type).
        """
        rows = []
        for element in array:
            if type(element) is not list:
                raise ValueError(
                    "The passed argument contains elements that are not a list;"
                    " these element cannot be converted into a MatrixRow"
                )

            rows.append(MatrixRow(element))

        return AugmentedMatrix(rows)

    def __init__(self, rows_list: list):
        """
        Constructor of the AugmentedMatrix class.

        :param rows_list: a list of MatrixRow, representing the different rows of the matrix.
        :type rows_list: list

        :raises ValueError: rows_list contains elements that are not instance of MatrixRow.
        """

        self.matrix = []

        for i in rows_list:
            if type(i) is not MatrixRow:
                raise ValueError(
                    "The row list passed to the constructor contains objects "
                    "that are not MatrixRow (\"{}\" is not a MatrixRow subtype).".format(type(i))
                )

            self.matrix.append(i)

    @property
    def length(self) -> int:
        """
        Get the number of lines in the matrix (and thus, its columns size)
        :return: The length of the inner list of rows
        :rtype: int
        """
        return len(self.matrix)

    def pretty_print(self):
        """
        Print the matrix in a more readable way.
        Note: This should be used for debugging only.
        """

        print("*** Matrix ***")
        for l in self.matrix:
            print("| ", end='')
            print("   ".join(str(i) for i in l), end=" |\n")
        print("*** ******* ***")

    def do_elimination(self):
        """
        Use row manipulations to transform the "first" matrix into an identity matrix,
        following the Gauss-Jordan algorithm.
        (the last column is not counted as part of the matrix identity,
        as it will hold the solutions of the system).

        :return: The last column, containing the solution (see AugmentedMatrix.get_last_column()).
        :rtype: tuple
        """

        # Gauss-Jordan algorithm translated in Python from the pseudo-code on the Wikipedia page
        # (more effective than my personal implementation).
        # Link : https://fr.wikipedia.org/wiki/%C3%89limination_de_Gauss-Jordan#Pseudocode

        r = -1
        for j in range(self.length):
            k = 0

            for i in range(r, self.length):
                if abs(self[k][j]) < abs(self[i][j]):
                    k = i

            if self[k][j] != 0:
                r += 1

                self[k].multiply_by_scalar(Fraction(1, self[k][j]))

                if k != r:
                    temp = self[k]
                    self[k] = self[r]
                    self[r] = temp

                for i in range(self.length):
                    if i != r:
                        self[i].add_row(self[r].get_multiplied_by_scalar(-self[i][j]))

    def __setitem__(self, key: int, value: MatrixRow):
        if type(key) is not int:
            raise ValueError("The key argument should be an integer")

        if type(value) is not MatrixRow:
            raise ValueError("The value given should be a MatrixRow instance")

        self.matrix[key] = value

    def __getitem__(self, item: int) -> MatrixRow:
        if type(item) is not int:
            raise ValueError("The key argument should be an integer")
        return self.matrix[item]

    def get_last_column(self) -> tuple:
        """
        get the last column of the augmented matrix (actually being the second matrix),
        containing the solutions if the solve method has been called once.

        :return: A tuple containing, from top to bottom, the values
                of the last column of the matrix.

        :rtype: tuple
        """
        return tuple([line[-1] for line in self.matrix])


def get_random_points(n: int, fro: int = 0, to: int = 255) -> list:
    """
    Get a list of random points; used for debugging purposes.
    Note : does not check input, as it has no real uses besides debugging verification.

    :param n: Number of points.
    :type n: int

    :param fro: Lowest value of the image.
    :type fro: int

    :param to: Biggest value of the image.
    :type to: int

    :return: a list of points.
    :rtype: list
    """
    return [(i + 1, randint(fro, to)) for i in range(n)]


def found_function(points: list) -> tuple:
    """
    Get the coefficients of a len(points)-1 polynomial equation
    that verifies P(x) = y, x and y being the two values of the tuples
    in the given list.

    :param points: points the function should verify; each item should be
        a tuple of length 2 ((x, y) <=> P(x) = y).
    :type points: list
    :return: the coefficients of the polynomial equations.
    :rtype: tuple

    :raises ValueError: if the list contains an item that is not a tuple of length 2.
    """

    # this function is a simple implementation of what AugmentedMatrix could be used for
    # It is a polynomial interpolation implementation :
    # it uses the fact that, for every list of n points (that differ from each other)
    # it exists a max. n-1 polynomial function that interpolate the whole data set.

    # get a matrix, as a 2-dimension array, from the different point

    matrix_array = []
    for point in points:

        # Each point is giving us an equation, that we will convert into a row of the
        # future augmented matrix.
        #
        # for instance, if we have three points, we have a degree-2 polynomial function
        # ax^2 + bx + c that interpolate them. So, for every point (let's take for instance (2, 1))
        # we compute the powers of x (in our case: 4, 2 and 1), which give us an equation
        # (in our example: 4a + 2b + c = 1), or a row of our augmented matrix ([4, 2, 1, 1]).

        row = []

        for i in range(len(points)):
            row.append(pow(point[0], i))

        row.reverse()
        row.append(point[1])
        matrix_array.append(MatrixRow(row))

    # get our object from the array
    matrix = AugmentedMatrix(matrix_array)

    # use the Gaussian elimination...
    matrix.do_elimination()

    # ...and retrieve our solutions !
    return matrix.get_last_column()


def main():

    # a little example :)

    print("3x + y - z = 9")
    print("2x - 2y + z = -3")
    print("x + y + z = 7")

    matrix_array = [
        [3, 1, -1, 9],
        [2, -2, 1, -3],
        [1, 1, 1, 7]
    ]

    matrix = AugmentedMatrix.wrap(matrix_array)
    print("Matrix representing the system :")
    matrix.pretty_print()

    matrix.do_elimination()
    solutions = matrix.get_last_column()

    print("solutions are : x = {} ; y = {} ; z = {}".format(*solutions))


main()
