import math


# Addition function
def add(*args):
    """
    Takes in any number of integer arguments, adds them, and returns the total.
    """
    total = 0
    for num in args:
        total += num

    return total


# Subtraction function
def sub(*args):
    """
    Takes in any number of integer arguments, subtracts them, and returns the total.
    **Anti-commutative - order of arguments matter.**
    """
    total = args[0]
    for num in args[1:-1]:
        total -= num

    return total


# Multiplication function
def mult(*args):
    """
    Takes in any number of integer arguments, multiplies them, and returns the product.
    """
    product = 1
    for num in args:
        product *= num

    return product


# Division function
def div(*args):
    """
    Takes in any number of integer arguments, divides them, and returns the quotient.
    **Anti-commutative - order of arguments matter.**
    """
    quotient = args[0]
    for num in args[1:-1]:
        quotient /= num

    return quotient


# Exponential function
def exp(x, n):
    """
    Takes in two argument, `x` and `n`, and returns `x` raised to the `n`-th power.
    """
    return x ** n


# Vector Class
class Vector:
    """
    Easier alternative to handling 2D and 3D vector quantities in Python.
    By default, z is 0 (for 2D handling).

    >>> v = Vector(3, 4)
    >>> v2 = Vector(6, 8)

    **Functions include:**


    **mag()** - magnitude of the vector

    >>> mag = v.mag()
    >>> print(mag)
    >>> 5

    **scale()** - scale a vector

    >>> v2.scale(2)
    >>> print(v2.x, v2.y, v2.z, v2.mag())
    >>> 12 16 0 20

    **add()/sub()** - Add/subtract a vector from current and save

    >>> v2.sub(v)
    >>> print(v2.x, v2.y, v2.z, v2.mag())
    >>> 9 12 0 15

    **add2()/sub2()** - Add/subtract a vector from current and return new Vector object

    >>> v_add_v2 = v.add2(v2)
    >>> print(v_add_v2.x, v_add_v2.y, v_add_v2.z, v_add_v2.mag())
    >>> 12 16 0 20

    **dist()** - Find Euclidean distance from two point (represented as Vector objects)

    >>> print(v.dist(v2))
    >>> 10

    """

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def mag(self):
        """
        Finds magnitude of vector using Pythagoras' theorem.
        """
        return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def normalize(self):
        """
        Normalizes a vector quantity, till it's magnitude it 1.
        """
        mag = self.mag()
        self.x /= mag
        self.y /= mag
        self.z /= mag

    def scale(self, factor):
        """
        Scales a vector using its factor parameter.
        """
        self.x *= factor
        self.y *= factor
        self.z *= factor

    def add(self, vector):
        """
        Adds an external Vector object to this Vector object, and saves.
        """
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def add2(self, vector):
        """
        Adds an external Vector object to this Vector object, and returns a new one.
        """
        x = self.x + vector.x
        y = self.y + vector.y
        z = self.z + vector.z
        return Vector(x, y, z)

    def sub(self, vector):
        """
        Subtracts an external Vector object by this Vector object, and saves.
        """
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

    def sub2(self, vector):
        """
        Adds an external Vector object by this Vector object, and returns a new one.
        """
        x = self.x - vector.x
        y = self.y - vector.y
        z = self.z - vector.z
        return Vector(x, y, z)

    def dist(self, vector):
        """
        Returns the Euclidean distance between two points (represented as Vector objects).
        """
        x = self.x - vector.x
        y = self.y - vector.y
        z = self.z - vector.z
        return Vector(x, y, z).mag()
