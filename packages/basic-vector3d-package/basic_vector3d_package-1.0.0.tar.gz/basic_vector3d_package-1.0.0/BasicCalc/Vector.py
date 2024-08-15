import math


class Vector3d:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def reverse(self):
        return Vector3d(-self._x, -self._y, -self._z)

    def normalization(self):
        length = math.sqrt(math.pow(self._x, 2) + math.pow(self._y, 2) + math.pow(self._z, 2))
        return Vector3d(self._x / length, self._y / length, self._z / length)

    def shift(self, direction, offset):
        if not isinstance(direction, Vector3d):
            raise TypeError("direction is not Vector3d object")
        if not isinstance(offset, float):
            raise TypeError("offset is not float object")
        norm = direction.normalization()
        return Vector3d(self._x + offset * norm.x, self._y + offset * norm.y, self._z + offset * norm.z)

    def __repr__(self):
        return f"Vector3d - ({self._x}, {self._y}, {self._z})"

    def __add__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return Vector3d(self._x + other.x, self._y + other.y, self._z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return Vector3d(self._x - other.x, self._y - other.y, self._z - other.z)

    def __eq__(self, other):
        if not isinstance(other, Vector3d):
            raise TypeError("other is not Vector3d object")
        return self._x == other.x and self._y == other.y and self._z == other.z




