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
        self.n = []
        self.v = []
        self.move()

        if isinstance(color[0], tuple):
            self.single_color = False

    def compute_normals(self):
        """
        Computes the normals for each face of the body.
        """

        self.n = [((self.v[face[2]] - self.v[face[0]]) @
                    (self.v[face[1]] - self.v[face[0]])).normalize() for face in self.f]


    def move(self, pos: Vec3 = None, rot: Quat = None, first_rotate: bool = True) -> None:
        """
        Move the body to a given position an with a certain rotation.
        If no arguments are passed will move the body according to the
        position and rotation stored in the instance.

        :param pos: target position, defaults to None
        :type pos: Vec3, optional
        :param rot: target rotation, defaults to None
        :type rot: Quat, optional
        """

        if pos is not None:
            self.pos = pos

        if rot is not None:
            self.rot = rot

        if first_rotate:
            self.v = [rotate(vertex, self.rot) + self.pos for vertex in self.vertices]
        else:
            self.v = [rotate(vertex + self.pos, self.rot) for vertex in self.vertices]

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

    @classmethod
    def sphere(
        cls,
        name: str,
        radius: float,
        quality: int = 1,
        pos: Vec3 = Vec3(0, 0, 0),
        rot: Quat = Quat(0, Vec3(0, 0, 1)),
        color: Color = WHITE) -> 'Body':
        """
        Constructor method that generates a sphere with a specific radius.

        :param name: unique name that identifies the body
        :type name: str
        :param radius: radius of the sphere
        :type radius: float
        :param quality: define the dfinition of the mesh, defaults to 1, minimum 0
        :type quality: int, optional
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

        t = (1 + 5 ** 0.5) / 2

        vertices = [
            Vec3(-1,  t,  0),
            Vec3( 1,  t,  0),
            Vec3(-1, -t,  0),
            Vec3( 1, -t,  0),
            Vec3( 0, -1,  t),
            Vec3( 0,  1,  t),
            Vec3( 0, -1, -t),
            Vec3( 0,  1, -t),
            Vec3( t,  0, -1),
            Vec3( t,  0,  1),
            Vec3(-t,  0, -1),
            Vec3(-t,  0,  1),
        ]

        faces = [
             (0, 11, 5),
             (0, 5, 1),
             (0, 1, 7),
             (0, 7, 10),
             (0, 10, 11),
             (1, 5, 9),
             (5, 11, 4),
             (11, 10, 2),
             (10, 7, 6),
             (7, 1, 8),
             (3, 9, 4),
             (3, 4, 2),
             (3, 2, 6),
             (3, 6, 8),
             (3, 8, 9),
             (4, 9, 5),
             (2, 4, 11),
             (6, 2, 10),
             (8, 6, 7),
             (9, 8, 1),
        ]

        mid_cache = dict()

        def get_mid_points(a, b):
            key = math.floor((a + b) * (a + b + 1) / 2) + min(a, b)

            if key in mid_cache:
                return mid_cache[key]

            mid_cache[key] = len(vertices)

            vertices.append(Vec3(
                (vertices[a].x + vertices[b].x) / 2,
                (vertices[a].y + vertices[b].y) / 2,
                (vertices[a].z + vertices[b].z) / 2,
            ))

            return len(vertices) - 1

        prev_faces = faces

        for i in range(quality):
            faces = [0] * (len(prev_faces) * 4)

            for k, face in enumerate(prev_faces):
                v1 = face[0]
                v2 = face[1]
                v3 = face[2]
                a = get_mid_points(v1, v2)
                b = get_mid_points(v2, v3)
                c = get_mid_points(v3, v1)
                faces[k * 4] = (v1, a, c)
                faces[k * 4 + 1] = (v2, b, a)
                faces[k * 4 + 2] = (v3, c, b)
                faces[k * 4 + 3] = (a, b, c)

            prev_faces = faces

        for i, vertex in enumerate(vertices):
            vertices[i] = vertex.normalize() * radius

        return cls(name, tuple(vertices), tuple(faces), pos, rot, color)


class Scene:
    """
    Class that contains the entities that will be rendered.

    :param bgc: background color, defaults to BLACK
    :type bgc: Color, optional
    :param bodies: dictionary of bodies that the scene has, defaults to None
    :type bodies: dict[str, Body], optional
    :param light: direction of the light
    :type light: Vec3
    """

    def __init__(self,
        bgc: Color = BLACK,
        bodies: dict[str, Body] = None,
        light: Vec3 = Vec3(0, 0, - 1)) -> None:

        self.bgc = bgc
        self.bodies = bodies
        self.light = light

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
        """
        Remove a body from the scene.

        :param name: unique name of the body to remove
        :type name: str
        """
        self.bodies.pop(name)
