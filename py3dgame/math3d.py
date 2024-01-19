"""
Module for simplify 3d math.
"""

from typing import Union
import math
import warnings


class Vec3:
    """
    3D vector class.

    :param x: x coordinate of the vector
    :type x: float
    :param y: y coordinate of the vector
    :type y: float
    :param z: z coordinate of the vector
    :type z: float
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vec3') -> 'Vec3':

        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vec3') -> 'Vec3':

        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> 'Vec3':

        return Vec3(- self.x, - self.y, - self.z)

    def __abs__(self) -> float:

        return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5

    def __mul__(self, other: Union[float, 'Vec3']) -> Union[float, 'Vec3']:

        if isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z

        return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> 'Vec3':

        return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float) -> 'Vec3':

        return Vec3(self.x / other, self.y / other, self.z / other)

    def __matmul__(self, other: 'Vec3') -> 'Vec3':
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        return Vec3(x, y, z)

    def normalize(self) -> 'Vec3':
        """
        Compute the normalized version of the vector.

        :return: normalized vector
        :rtype: Vec3
        """

        return self / abs(self)

    def __eq__(self, other: 'Vec3') -> bool:
        return (math.isclose(self.x, other.x, abs_tol=1e-12) and
                math.isclose(self.y, other.y, abs_tol=1e-12) and
                math.isclose(self.z, other.z, abs_tol=1e-12))

    def __str__(self):
        return f"Vec3: (x: {self.x:.4f}, y: {self.y:.4f}, z: {self.z:.4f})"


class Quat:
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
        self.w = math.cos(angle / 2)
        self.x = self.axis.x * math.sin(angle / 2)
        self.y = self.axis.y * math.sin(angle / 2)
        self.z = self.axis.z * math.sin(angle / 2)

    def __str__(self):
        return f"Quat: (w: {self.w:.4f}, x: {self.x:.4f}, y: {self.y:.4f}, z: {self.z:.4f})"

    @classmethod
    def from_coord(cls, w: float, x: float, y: float, z: float) -> 'Quat':
        """
        Generate a :class:`Quat` from its coordinates.

        :param w: w coordinate
        :type w: float
        :param x: x coordinate
        :type x: float
        :param y: y coordinate
        :type y: float
        :param z: z coordinate
        :type z: float
        :return: resulting quaternion
        :rtype: Quat
        """

        quat = cls(0)
        quat.w = w
        quat.x = x
        quat.y = y
        quat.z = z

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

        return cls.from_coord(w, x, y, z)

    def to_vec3(self) -> Vec3:
        """
        Convert the :class:`Quat` to a :class:`Vec3`.
        If the actual :class:`Quat` is (w, x, y, z) the resulting
        :class:`Vec3` will be (x, y, z).

        :return: new vector
        :rtype: Vec
        """

        return Vec3(self.x, self.y, self.z)

    def inverse(self) -> 'Quat':
        """
        Compute the inverse of a :class:`Quat`.
        The inverse of q = (w, x, y, z) is computed as
        q^(- 1) = (w, - x, - y, - z) / (|q|)^2

        :return: inverse quaternion
        :rtype: Quat
        """

        return Quat.from_coord(self.w, - self.x, - self.y, - self.z) / abs(self) / abs(self)

    def __add__(self, other: 'Quat') -> 'Quat':

        return Quat.from_coord(self.w + other.w,
                               self.x + other.x,
                               self.y + other.y,
                               self.z + other.z)

    def __sub__(self, other: 'Quat') -> 'Quat':

        return Quat.from_coord(self.w - other.w,
                               self.x - other.x,
                               self.y - other.y,
                               self.z - other.z)

    def __neg__(self) -> 'Quat':

        return Quat.from_coord(- self.w, - self.x, - self.y, - self.z)

    def __abs__(self) -> float:

        return (self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5

    def __mul__(self, other: 'Quat') -> 'Quat':
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w

        return Quat.from_coord(w, x, y, z)

    def __truediv__(self, other: float) -> 'Quat':

        return Quat.from_coord(self.w / other, self.x / other, self.y / other, self.z / other)

    def __eq__(self, other: 'Quat') -> bool:
        return (math.isclose(self.w, other.w, abs_tol=1e-12) and
                math.isclose(self.x, other.x, abs_tol=1e-12) and
                math.isclose(self.y, other.y, abs_tol=1e-12) and
                math.isclose(self.z, other.z, abs_tol=1e-12))


class Mat:
    """
    3D matrix class.

    :param r1: first row of the matrix
    :type r1: Vec3
    :param r2: second row of the matrix
    :type r2: Vec3
    :param r3: third row of the matrix
    :type r3: Vec3
    """

    def __init__(self, r1: Vec3, r2: Vec3, r3: Vec3) -> None:
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3

    def det(self) -> float:
        """
        Computes the determinant of the matrix.

        :return: determinant
        :rtype: float
        """

        det = (self.r1.x * self.r2.y * self.r3.z +
               self.r2.x * self.r3.y * self.r1.z +
               self.r3.x * self.r1.y * self.r2.z -
               self.r1.x * self.r3.y * self.r2.z -
               self.r2.x * self.r1.y * self.r3.z -
               self.r3.x * self.r2.y * self.r1.z)

        if math.isclose(0, det, abs_tol=1e-9):
            warnings.warn(f"Determinant equal to {det}, the matrix may be singular!")

        return det

    def inverse(self) -> 'Mat':
        """
        Computes the inverse of the matrix.

        :return: inverted matrix
        :rtype: Mat
        """

        det = self.det()
        r1 = Vec3(
            self.r2.y * self.r3.z - self.r3.y * self.r2.z,
            self.r3.y * self.r1.z - self.r1.y * self.r3.z,
            self.r1.y * self.r2.z - self.r2.y * self.r1.z
        ) / det
        r2 = Vec3(
            self.r3.x * self.r2.z - self.r2.x * self.r3.z,
            self.r1.x * self.r3.z - self.r3.x * self.r1.z,
            self.r2.x * self.r1.z - self.r1.x * self.r2.z
        ) / det
        r3 = Vec3(
            self.r2.x * self.r3.y - self.r3.x * self.r2.y,
            self.r3.x * self.r1.y - self.r1.x * self.r3.y,
            self.r1.x * self.r2.y - self.r2.x * self.r1.y
        ) / det

        return Mat(r1, r2, r3)

    def __matmul__(self, other: Vec3) -> Vec3:
        return Vec3(self.r1 * other, self.r2 * other, self.r3 * other)


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
