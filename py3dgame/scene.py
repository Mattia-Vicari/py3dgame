"""
Implementations of every object that is contained in a scene.
"""

from .color import Color
from .math3d import Vec3, Quat, rotate
import math


class Body:
    """
    _summary_

    :param v: _description_
    :type v: tuple[Vec]
    """

    def __init__(
        self, vertices: tuple[Vec3],
        faces: tuple[tuple[int]],
        pos: Vec3 = Vec3(0, 0, 0),
        rot: Quat = Quat(0, Vec3(0, 0, 1)),
        color: tuple = Color.white) -> None:

        self.vertices = vertices
        self.f = faces
        self.pos = pos
        self.rot = rot
        self.color = color
        self.single_color = True
        self.move()

        if isinstance(color[0], tuple):
            self.single_color = False

    def compute_normals(self):
        normals = []
        for face in self.f:
            v1 = self.v[face[1]] - self.v[face[0]]
            v2 = self.v[face[2]] - self.v[face[0]]
            normals.append(v2 @ v1)

        self.n = tuple(normals)

    def move(self, pos: Vec3 = None, rot: Quat = None) -> None:
        v = []

        if pos is not None:
            self.pos = pos

        if rot is not None:
            self.rot = rot

        for vertex in self.vertices:
            v.append(rotate(vertex + self.pos, self.rot))

        self.v = v
        self.compute_normals()

    def rotate(self, angle: float) -> None:
        self.rot = Quat(self.rot.angle + angle, self.rot.axis)
        self.move()

    def rotate_deg(self, angle: float) -> None:
        self.rotate(angle * math.pi / 180)

    @classmethod
    def from_obj(cls, obj_file: str) -> 'Body':
        """
        Generate a :class:`Body` from a .obj file.

        :param obj_file: path to the .obj file
        :type obj_file: str
        :rtype: Body
        """

        vertices = ...
        faces = ...

        return cls(vertices, faces)

    @classmethod
    def cube(
        cls, dim: float,
        pos: Vec3 = Vec3(0, 0, 0),
        rot: Quat = Quat(0, Vec3(0, 0, 1)),
        color: tuple = Color.white) -> 'Body':
        """
        Constructor method that generates a cube with a specific dimension.

        :param dim: length of the cube edges
        :type dim: float
        :param pos: position of the origin of the body in the world reference system,
            defaults to (0, 0, 0)
        :type pos: tuple[float], optional
        :param color: if a tuple with 3 values is used each face of the body will use that color,
            to assign a specific color to each face use a `tuple` containing 6 `tuples`
            representing the RGB triplet for each face, defaults to Color.white
        :type color: tuple, optional
        :rtype: Body
        """

        dim = dim / 2
        vertices = (
            Vec3(dim, dim, dim),
            Vec3(dim, - dim, - dim),
            Vec3(dim, dim, - dim),
            Vec3(dim, - dim, dim),
            Vec3(- dim, dim, - dim),
            Vec3(- dim, dim, dim),
            Vec3(- dim, - dim, dim),
            Vec3(- dim, - dim, - dim)
        )
        faces = (
            (0, 1, 2),
            (0, 3, 1),
            (1, 3, 6),
            (1, 6, 7),
            (5, 0, 2),
            (5, 2, 4),
            (6, 5, 4),
            (7, 6, 4),
            (0, 5, 6),
            (0, 6, 3),
            (2, 7, 4),
            (2, 1, 7)
        )

        if isinstance(color[0], tuple):
            color = (
                color[0],
                color[0],
                color[1],
                color[1],
                color[2],
                color[2],
                color[3],
                color[3],
                color[4],
                color[4],
                color[5],
                color[5]
            )

        return cls(vertices, faces, pos, rot, color)


class Scene:
    def __init__(self, bgc: Color = Color.black,  bodies: list[Body] = []) -> None:
        self.bgc = bgc
        self.bodies = bodies

    def add_body(self, body: Body) -> None:
        self.bodies.append(body)
