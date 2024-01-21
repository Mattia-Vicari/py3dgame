"""
Module for handling the rendering pipeline.
"""

import math
import ctypes
import platform
import pygame
import numpy as np
from .math3d import Vec3, Quat, rotate
from .color import WHITE, darken_color, Color
from .scene import Scene, Body


class Camera:
    """
    Class to handle the camera postion for the rendering.

    :param pos: initial position of the camera, defaults to Vec3(0, 0, 0)
    :type pos: Vec3, optional
    :param direction: initial direction of the camera, defaults to Vec3(1, 0, 0)
    :type direction: Vec3, optional
    """

    def __init__(
            self,
            pos: Vec3 = Vec3(0, 0, 0),
            direction: Vec3 = Vec3(1, 0, 0)) -> None:

        self.pos = pos
        self.dir = direction
        self.zoom = 1000
        self.mouse_pos = None

        self.theta = math.pi / 2
        self.zfar = 1000
        self.znear = 0.1

        self.w = 0
        self.h = 0
        self.a = 0
        self.f = 0
        self.q = 0
        self.af = 0
        self.up = Vec3(0, 0, 0)
        self.right = Vec3(0, 0, 0)
        self.tup = 0
        self.tdir = 0
        self.tright = 0

    def handle_movements(self, fps: float) -> None:
        """
        Move the mare position with A, W, S, D or the arrows and the
        change the rotation using the mouse.
        """

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos = self.pos - self.right / fps

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos = self.pos + self.right / fps

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos = self.pos + self.dir / fps

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos = self.pos - self.dir / fps

        if mouse_buttons[1]:
            if self.mouse_pos is not None:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = Vec3(mouse_pos[0], mouse_pos[1], 0)
                angle = (self.mouse_pos - mouse_pos).x / 1000
                self.dir = rotate(self.dir, Quat(angle, self.up))
                self.update_view_space()

                angle = (self.mouse_pos - mouse_pos).y / 1000
                self.dir = rotate(self.dir, Quat(angle, self.right))
                self.update_view_space()

            mouse_pos = pygame.mouse.get_pos()
            self.mouse_pos = Vec3(mouse_pos[0], mouse_pos[1], 0)
        else:
            self.mouse_pos = None

    def update_projection_space(self, screen: pygame.Surface) -> None:
        """
        Update parameters for the computing the screen space.

        :param screen: screen of the active window
        :type screen: pygame.Surface
        """

        self.w = screen.get_width()
        self.h = screen.get_height()
        self.a = self.h / self.w
        self.f = 1 / math.tan(self.theta / 2)
        self.q = self.zfar / (self.zfar - self.znear)
        self.af = self.a * self.f

    def update_view_space(self) -> None:
        """
        Update parameters to compute the view space.
        """

        up = Vec3(0, 0, 1)
        self.up = (up - (self.dir * (up * self.dir))).normalize()
        self.right = self.dir @ self.up

        target = self.pos + self.dir

        self.tup = target * self.up
        self.tdir = target * self.dir
        self.tright = target * self.right


class Renderer:
    """
    Class that handles the rendering.

    :param screen: pygame window of the application
    :type screen: pygame.Surface
    :param camera: camera that will render
    :type camera: Camera
    :param scene: scene to be rendered
    :type scene: Scene
    :param clock: pygame clock
    :type clock: pygame.time.Clock
    :param caption: caption of the window, defaults to "Py3dGame"
    :type caption: str, optional
    """

    pygame.init()
    font = pygame.font.SysFont('arial', 18, True)

    def __init__(
        self,
        screen: pygame.Surface,
        camera: Camera,
        scene: Scene,
        clock: pygame.time.Clock,
        caption: str = "Py3dGame") -> None:

        self.screen = screen
        self.camera = camera
        self.scene = scene
        self.screen.fill(self.scene.bgc)
        self.clock = clock
        self.queue = []
        self.triangles = 0
        self.computed = dict()
        self.buffer = pygame.surfarray.array3d(self.screen)
        self.depth = np.ones((self.buffer.shape[0],
                              self.buffer.shape[1]),
                              dtype=np.float32) * self.camera.zfar
        self.buffer.flags.writeable = True
        self.depth.flags.writeable = True
        self.buffer_ptr = self.buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        self.depth_ptr = self.depth.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        if platform.system() == "Windows":
            self.lib = ctypes.CDLL("lib/rendering.dll")

        self.lib.draw_triangle.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_int, ctypes.c_int,
            ctypes.c_float, ctypes.c_float, ctypes.c_float,
            ctypes.c_float, ctypes.c_float, ctypes.c_float,
            ctypes.c_float, ctypes.c_float, ctypes.c_float,
            ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8,
            ctypes.c_int, ctypes.c_int
        ]
        self.lib.draw_triangle.restype = None

        self.lib.fill_bg.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8,
            ctypes.c_int, ctypes.c_int
        ]
        self.lib.fill_bg.restype = None

        pygame.display.set_caption(caption)

    def render(self) -> None:
        """
        Render all the object in scene.
        """

        self.triangles = 0
        self.camera.update_projection_space(self.screen)
        self.camera.update_view_space()
        self.computed = dict()
        self.lib.fill_bg(
            self.buffer_ptr,
            self.buffer.strides[0], self.buffer.strides[1], self.buffer.strides[2],
            ctypes.c_uint8(self.scene.bgc[0]),
            ctypes.c_uint8(self.scene.bgc[1]),
            ctypes.c_uint8(self.scene.bgc[2]),
            ctypes.c_int(self.camera.w), ctypes.c_int(self.camera.h)
        )
        self.depth.fill(self.camera.zfar)

        for body in self.scene.bodies.values():
            self.render_body(body)

        self.screen.blit(pygame.surfarray.make_surface(self.buffer), (0, 0))

        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {fps:.2f}", True, WHITE)
        tri_text = self.font.render(f"Triangles: {self.triangles}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        self.screen.blit(tri_text, (10, 30))

        pygame.display.flip()


    def render_body(self, body: Body):
        """
        Render a specific body.

        :param body: body to render
        :type body: Body
        """

        for i, normal in enumerate(body.n):
            cam_to_vertex = body.v[body.f[i][0]] - self.camera.pos

            if cam_to_vertex * normal > 0:
                self.render_face(body, i)

    def project_point(self, point: Vec3) -> tuple[float, float, float]:
        """
        Project point from view space to screen space.

        :param point: point in view space
        :type point: Vec3
        :return: point in screen space
        :rtype: tuple[float, float, float]
        """

        x = self.camera.af * point.x
        y = self.camera.f * point.y
        z = self.camera.q * (point.z - self.camera.znear)

        if point.z != 0:
            return (x / point.z, y / point.z, z)

        return (x, y, z)

    def to_view_space(self, point: Vec3) -> Vec3:
        """
        Convert point from world coordinates to view space.

        :param point: point in world coordinates
        :type point: Vec3
        :return: point in view space
        :rtype: Vec3
        """

        x = point * self.camera.right - self.camera.tright
        y = point * self.camera.up - self.camera.tup
        z = point * self.camera.dir - self.camera.tdir

        return Vec3(x, y, z)

    def render_face(self, body: Body, i: int) -> None:
        """
        Render a specific face.

        :param body: body that contain the face
        :type body: Body
        :param i: index of the face
        :type i: int
        """

        if body.f[i][0] in self.computed:
            point1 = self.computed[body.f[i][0]]
        else:
            point1 = self.to_view_space(body.v[body.f[i][0]])
            point1 = self.project_point(point1)
            point1 = (
                (point1[0] + 1) / 2 * self.camera.w,
                (- point1[1] + 1) / 2 * self.camera.h,
                point1[2]
            )
            self.computed[body.f[i][0]] = point1

        if body.f[i][1] in self.computed:
            point2 = self.computed[body.f[i][1]]
        else:
            point2 = self.to_view_space(body.v[body.f[i][1]])
            point2 = self.project_point(point2)
            point2 = (
                (point2[0] + 1) / 2 * self.camera.w,
                (- point2[1] + 1) / 2 * self.camera.h,
                point2[2]
            )
            self.computed[body.f[i][1]] = point2

        if body.f[i][2] in self.computed:
            point3 = self.computed[body.f[i][2]]
        else:
            point3 = self.to_view_space(body.v[body.f[i][2]])
            point3 = self.project_point(point3)
            point3 = (
                (point3[0] + 1) / 2 * self.camera.w,
                (- point3[1] + 1) / 2 * self.camera.h,
                point3[2]
            )
            self.computed[body.f[i][2]] = point3

        if (point1[0] > self.camera.w and
            point2[0] > self.camera.w and
            point3[0] > self.camera.w):
            return

        if (point1[0] < 0 and
            point2[0] < 0 and
            point3[0] < 0):
            return

        if (point1[1] > self.camera.h and
            point2[1] > self.camera.h and
            point3[1] > self.camera.h):
            return

        if (point1[1] < 0 and
            point2[1] < 0 and
            point3[1] < 0):
            return

        if (point1[2] < self.camera.znear or
            point2[2] < self.camera.znear or
            point3[2] < self.camera.znear):
            return

        if (point1[2] > self.camera.zfar or
            point2[2] > self.camera.zfar or
            point3[2] > self.camera.zfar):
            return


        points = (
            point1,
            point2,
            point3
        )

        light_intensity = (body.n[i] * self.scene.light) / 2 + 0.5

        if body.single_color:
            self.draw_triangle(points[0], points[1], points[2],
                               darken_color(body.color, light_intensity))
        else:
            self.draw_triangle(points[0], points[1], points[2],
                               darken_color(body.color[i], light_intensity))

        self.triangles += 1

    def draw_triangle(
        self,
        p1: tuple[int, int, float],
        p2: tuple[int, int, float],
        p3: tuple[int, int, float],
        color: Color) -> None:
        """
        Draw a triangle using the pixel buffer.

        :param p1: point 1
        :type p1: tuple[float, float]
        :param p2: point 2
        :type p2: tuple[float, float]
        :param p3: point 3
        :type p3: tuple[float, float]
        :param color: color of the triangle
        :type color: Color
        """

        self.lib.draw_triangle(
            self.buffer_ptr,
            self.buffer.strides[0], self.buffer.strides[1], self.buffer.strides[2],
            self.depth_ptr,
            self.depth.strides[0], self.depth.strides[1],
            p1[0], p1[1], p1[2],
            p2[0], p2[1], p2[2],
            p3[0], p3[1], p3[2],
            color[0], color[1], color[2],
            self.camera.w, self.camera.h
        )
