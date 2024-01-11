"""
Module for simplify 3d math.
"""

from typing import Union, Iterable
import math
import numpy as np


class Vec:
    """
    Generic vector class to handle geometry operations.

    :param array: array of floats
    :type array: Iterable[float]
    """

    def __init__(self, array: Iterable[float]) -> None:
        self._vec = np.array(array)

    # mathematical operators
    def __add__(self, other: 'Vec') -> 'Vec':
        return self.__class__.from_array(self._vec + other._vec)

    def __sub__(self, other: 'Vec' = 0) -> 'Vec':
        return self.__class__.from_array(self._vec - other._vec)

    def __neg__(self) -> 'Vec':
        return self.__class__.from_array(- self._vec)

    def __abs__(self) -> float:
        return sum(self._vec ** 2) ** 0.5

    def __mul__(self, other: Union[float, 'Vec']) -> Union[float, 'Vec']:
        if isinstance(other, Vec):
            return sum(self._vec * other._vec)

        return self.__class__.from_array(self._vec * other)

    def __rmul__(self, other: float) -> 'Vec':
        return self.__class__.from_array(self._vec * other)

    def __truediv__(self, other: float) -> 'Vec':
        return self.__class__.from_array(self._vec / other)

    def __matmul__(self, other: 'Vec') -> 'Vec':
        return self.__class__.from_array(np.cross(self._vec, other._vec))

    def normalize(self) -> 'Vec':
        """
        Compute the normalized version of the vector.

        :return: normalized vector
        :rtype: Vec
        """

        return self / abs(self)

    # boolean operators
    def __eq__(self, other: 'Vec'):
        return np.allclose(self._vec, other._vec)

    def __str__(self):
        return self._vec.__str__()

    def to_nparray(self) -> np.ndarray:
        """
        Convert the :class:`Vec` instance to a `np.ndarray`.

        :return: numpy array with the same elements
        :rtype: np.ndarray
        """

        return self._vec

    @classmethod
    def from_array(cls, array: Iterable[float]) -> 'Vec':
        """
        Constructor equal to the __init__ method.
        This is needed just for inheritance purposes

        :param array: array of floats
        :type array: Iterable[float]
        :return: instance of the class
        :rtype: Vec
        """
        return cls(np.array(array))


class Vec3(Vec):
    """
    3D vector class that extends :class:`Vec`.

    :param x: x coordinate of the vector
    :type x: float
    :param y: y coordinate of the vector
    :type y: float
    :param z: z coordinate of the vector
    :type z: float
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__((x, y, z))

    @property
    def x(self) -> float:
        """
        Allow access to the x cordinate of the vector.
        """

        return self._vec[0]

    @x.setter
    def x(self, new_value: float) -> None:
        self._vec[0] = new_value

    @property
    def y(self) -> float:
        """
        Allow access to the y cordinate of the vector.
        """

        return self._vec[1]

    @y.setter
    def y(self, new_value: float) -> None:
        self._vec[1] = new_value

    @property
    def z(self) -> float:
        """
        Allow access to the z cordinate of the vector.
        """

        return self._vec[2]

    @z.setter
    def z(self, new_value: float) -> None:
        self._vec[2] = new_value

    def __str__(self):
        return f"(x: {self.x:.4f}, y: {self.y:.4f}, z: {self.z:.4f})"

    @classmethod
    def from_array(cls, array: Iterable) -> 'Vec3':
        return cls(array[0], array[1], array[2])


class Quat(Vec):
    """
    Quaternion class for performing geometric rotations.
    For this reason the queaternions will be generated using an angle and an axis definition.

    :param angle: angle in radians of rotation around the axis
    :type angle: float
    :param axis: vector that represent the axis of the rotation
    :type axis: Vec3
    """

    def __init__(self, angle: float, axis: Vec3 = Vec3(0, 0, 1)) -> None:
        self.axis = axis.normalize()
        self.angle = angle
        w = math.cos(angle / 2)
        x = self.axis.x * math.sin(angle / 2)
        y = self.axis.y * math.sin(angle / 2)
        z = self.axis.z * math.sin(angle / 2)
        super().__init__((w, x, y, z))

    @property
    def w(self) -> float:
        """
        Allow access to the w cordinate of the vector.
        """

        return self._vec[0]

    @w.setter
    def w(self, new_value: float) -> None:
        self._vec[0] = new_value

    @property
    def x(self) -> float:
        """
        Allow access to the x cordinate of the vector.
        """

        return self._vec[1]

    @x.setter
    def x(self, new_value: float) -> None:
        self._vec[1] = new_value

    @property
    def y(self) -> float:
        """
        Allow access to the y cordinate of the vector.
        """

        return self._vec[2]

    @y.setter
    def y(self, new_value: float) -> None:
        self._vec[2] = new_value

    @property
    def z(self) -> float:
        """
        Allow access to the z cordinate of the vector.
        """

        return self._vec[3]

    @z.setter
    def z(self, new_value: float) -> None:
        self._vec[3] = new_value

    def __str__(self):
        return f"(w: {self.w:.4f}, x: {self.x:.4f}, y: {self.y:.4f}, z: {self.z:.4f})"

    @classmethod
    def from_array(cls, array: Iterable) -> 'Quat':
        quat = cls(0)
        quat.w = array[0]
        quat.x = array[1]
        quat.y = array[2]
        quat.z = array[3]

        return quat

    @classmethod
    def from_vec3(cls, vec: Vec3) -> 'Quat':
        """
        Generate a :class:`Quat` from a :class:`Vec3`.
        If the given :class:`Vec3` is (x, y, z) the resulting
        :class:`Quat` will be (0, x, y, z).

        :param vec: initial vector
        :type vec: Vec3
        :return: resulting quaternion
        :rtype: Quat
        """

        w = 0
        x = vec.x
        y = vec.y
        z = vec.z

        return cls.from_array((w, x, y, z))

    def to_vec3(self) -> Vec:
        """
        Convert the :class:`Quat` to a :class:`Vec3`.
        If the actual :class:`Quat` is (w, x, y, z) the resulting
        :class:`Vec3` will be (x, y, z).

        :return: new vector
        :rtype: Vec
        """

        return Vec3(self.x, self.y, self.z)

    def __mul__(self, other: 'Quat') -> 'Quat':
        mat = np.array((
            (other.w, other.x, other.y, other.z),
            (- other.x, other.w, - other.z, other.y),
            (- other.y, other.z, other.w, - other.x),
            (- other.z, - other.y, other.x, other.w)
        ))

        return self.__class__.from_array(self._vec @ mat)

    def inverse(self) -> 'Quat':
        """
        Compute the inverse of a :class:`Quat`.
        The inverse of q = (w, x, y, z) is computed as
        q^(- 1) = (w, - x, - y, - z) / (|q|)^2

        :return: inverse quaternion
        :rtype: Quat
        """

        return self.__class__.from_array((self.w, - self.x, - self.y, - self.z)) / abs(self) ** 2


def rotate(vec: Vec3, quat: Quat):
    """
    Performs the rotation of a vector given a rotation quaternion.

    :param vec: original vector that needs to be rotated
    :type vec: Vec3
    :param quat: quaternion representing a rotation with a
        certain angle around a certain axis
    :type quat: Quat
    :return: rotated vector
    :rtype: _type_
    """

    vec = Quat.from_vec3(vec)
    new_quat = quat.inverse() * vec * quat

    return new_quat.to_vec3()
