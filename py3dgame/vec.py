import numpy as np
from typing import Union


class Vec:
    def __init__(self, x: float, y: float, z: float) -> None:
        self._vec = np.array((x, y, z))

    @property
    def x(self) -> float:
        return self._vec[0]

    @x.setter
    def x(self, new_value: float) -> None:
        self._vec[0] = new_value

    @property
    def y(self) -> float:
        return self._vec[1]

    @y.setter
    def y(self, new_value: float) -> None:
        self._vec[1] = new_value

    @property
    def z(self) -> float:
        return self._vec[2]

    @z.setter
    def z(self, new_value: float) -> None:
        self._vec[2] = new_value

    # mathematical operators
    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec.from_array(self._vec + other._vec)

    def __sub__(self, other: 'Vec') -> 'Vec':
        return Vec.from_array(self._vec - other._vec)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2  + self.z ** 2) ** 0.5

    def __mul__(self, other: Union[float, 'Vec']) -> Union[float, 'Vec']:
        if isinstance(other, Vec):
            return sum(self._vec * other._vec)
        else:
            return Vec.from_array(self._vec * other)

    def __rmul__(self, other: float) -> 'Vec':
        return Vec.from_array(self._vec * other)

    def __matmul__(self, other: 'Vec') -> 'Vec':
        return Vec.from_array(np.cross(self._vec, other._vec))

    # boolean operators
    def __eq__(self, other: 'Vec'):
        return self.x == other.x and self.y == other.y and self.z == other.z

    @classmethod
    def from_array(cls, array: np.ndarray) -> 'Vec':
        return Vec(array[0], array[1], array[2])