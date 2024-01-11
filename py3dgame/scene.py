"""
Implementations of the scene and objects that can contain.
"""

import math
from typing import Union
from .color import WHITE, BLACK, Color
from .math3d import Vec3, Quat, rotate


class Body:
    """
    Class to store information about physical entities.

    :param name: unique name that identifies the body
    :type name: str
    :param vertices: vertices of the body
    :type vertices: tuple[Vec3]
    :param faces: faces of the body as tuples of indexes of the vertices
    :type faces: tuple[tuple[int]]
    :param pos: initial position of the body, defaults to Vec3(0, 0, 0)
    :type pos: Vec3, optional
    :param rot: initial roatation of the body, defaults to Quat(0, Vec3(0, 0, 1))
    :type rot: Quat, optional
    :param color: color of the body, can be a single color or a tuple
        with one color for each face, defaults to color.WHITE
    :type color: Color, tuple[Color], optional
    """

    def __init__(
        self,
        name: str,
        vertices: tuple[Vec3],
        faces: tuple[tuple[int, int, int]],
        pos: Vec3 = Vec3(0, 0, 0),
        rot: Quat = Quat(0, Vec3(0, 0, 1)),
        color: Union[Color, tuple[Color]] = WHITE) -> None:

        self.name = name
        self.vertices = vertices
        self.f = faces
        self.pos = pos
        self.rot = rot
        self.color = color
        self.single_color = True
        self.n = ()
        self.v = ()
        self.move()

        if isinstance(color[0], tuple):
            self.single_color = False

    def compute_normals(self):
        """
        Computes the normals for each face of the body.
        """

        normals = []
        for face in self.f:
            v1 = self.v[face[1]] - self.v[face[0]]
            v2 = self.v[face[2]] - self.v[face[0]]
            normals.append(v2 @ v1)

        self.n = tuple(normals)

    def move(self, pos: Vec3 = None, rot: Quat = None) -> None:
        """
        Move the body to a given position an with a certain rotation.
        If no arguments are passed will move the body according to the
        position and rotation stored in the instance.

        :param pos: target position, defaults to None
        :type pos: Vec3, optional
        :param rot: target rotation, defaults to None
        :type rot: Quat, optional
        """

        v = []

        if pos is not None:
            self.pos = pos

        if rot is not None:
            self.rot = rot

        for vertex in self.vertices:
            v.append(rotate(vertex + self.pos, self.rot))

        self.v = v
        self.compute_normals()

    def traslate(self, pos: Vec3):
        """
        Traslate the body of a certain amout with
        respect to the current position.

        :param pos: traslation amount
        :type pos: Vec3
        """

        self.pos = self.pos + pos
        self.move()

    def rotate(self, angle: float) -> None:
        """
        Rotate around the current axis of a given
        amount starting from the actual one.

        :param angle: angle in rad
        :type angle: float
        """

        self.rot = Quat(self.rot.angle + angle, self.rot.axis)
        self.move()

    def rotate_deg(self, angle: float) -> None:
        """
        Rotate around the current axis of a given
        amount starting from the actual one.

        :param angle: angle in rad
        :type angle: float
        """
        self.rotate(angle * math.pi / 180)

    @classmethod
    def from_obj(cls, obj_file: str, name: str = None) -> 'Body':  # TODO
        """
        Generate a :class:`Body` from a .obj file.

        :param obj_file: path to the .obj file
        :type obj_file: str
        :return: instance of the class
        :rtype: Body
        """

        pos = Vec3(0, 0, 0)
        rot = Quat(0, Vec3(0, 0, 1))

        if name is None:
            name = obj_file

        vertices = ...
        faces = ...

        return cls(name, vertices, faces, pos, rot, WHITE)

    @classmethod
    def cube(
        cls,
        name: str,
        dim: float,
        pos: Vec3 = Vec3(0, 0, 0),
        rot: Quat = Quat(0, Vec3(0, 0, 1)),
        color: Color = WHITE) -> 'Body':
        """
        Constructor method that generates a cube with a specific dimension.

        :param name: unique name that identifies the body
        :type name: str
        :param dim: length of the cube edges
        :type dim: float
        :param pos: position of the origin of the body in the world reference system,
            defaults to (0, 0, 0)
        :type pos: tuple[float], optional
        :param color: if a tuple with 3 values is used each face of the body will use that color,
            to assign a specific color to each face use a `tuple` containing 6 `tuples`
            representing the RGB triplet for each face, defaults to Color.white
        :type color: tuple, optional
        :return: instance of the class
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

        return cls(name, vertices, faces, pos, rot, color)


class Scene:
    """
    Class that contains the entities that will be rendered.

    :param bgc: background color, defaults to BLACK
    :type bgc: Color, optional
    :param bodies: dictionary of bodies that the scene has, defaults to None
    :type bodies: dict[str, Body], optional
    """

    def __init__(self, bgc: Color = BLACK,  bodies: dict[str, Body] = None) -> None:

        self.bgc = bgc
        self.bodies = bodies

    def add_body(self, body: Body) -> None:
        """
        Add a body to the scene.

        :param body: body
        :type body: Body
        """

        if self.bodies is None:
            self.bodies = {body.name: body}
        else:
            self.bodies[body.name] = body

    def remove_body(self, name: str) -> None:
        """_summary_

        :param name: _description_
        :type name: str
        """
        self.bodies.pop(name)
