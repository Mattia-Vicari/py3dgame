"""
Module for handling the rendering pipeline.
"""

import math
from collections import defaultdict
import pygame
import numpy as np
from ext_rendering import draw_triangle, fill_bg
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

    __slots__ = ["pos", "dir", "mouse_pos",
                 "theta", "zfar", "znear",
                 "w", "h", "a", "f", "q", "af",
                 "up", "right", "tup", "tright", "tdir"]

    def __init__(
            self,
            pos: Vec3 = Vec3(0, 0, 0),
            direction: Vec3 = Vec3(1, 0, 0)) -> None:

        self.pos = pos
        self.dir = direction
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

    __slots__ = ["screen", "camera", "scene", "clock", "triangles", "computed",
                 "lib", "buffer", "depth", "buffer_ptr", "depth_ptr"]

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
        self.triangles = 0
        self.computed = defaultdict(self._default_value)
        self.buffer = pygame.surfarray.array3d(self.screen)
        self.depth = np.ones((self.buffer.shape[0],
                              self.buffer.shape[1]),
                              dtype=np.float32) * self.camera.zfar
        self.buffer.flags.writeable = True
        self.depth.flags.writeable = True
        self.buffer_ptr = self.buffer.__array_interface__['data'][0]
        self.depth_ptr = self.depth.__array_interface__['data'][0]

        pygame.display.set_caption(caption)

    @staticmethod
    def _default_value() -> None:
        return None

    def render(self) -> None:
        """
        Render all the object in scene.
        """

        self.triangles = 0
        self.camera.update_projection_space(self.screen)
        self.camera.update_view_space()
        self.computed = defaultdict(self._default_value)
        fill_bg(
            self.buffer_ptr,
            *self.buffer.strides,
            *self.scene.bgc, self.camera.w, self.camera.h
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
            face = body.f[i]
            cam_to_vertex = body.v[face[0]] - self.camera.pos

            if cam_to_vertex * normal > 0:

                if body.single_color:
                    color = body.color
                else:
                    color = body.color[i]

                self.render_face(body, face, normal, color)

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
            x = x / point.z
            y = y / point.z

        x = (x + 1) / 2 * self.camera.w
        y = (- y + 1) / 2 * self.camera.h

        return (x, y, z)

    def render_face(self,
        body: Body,
        face: tuple[int, int, int],
        normal: Vec3,
        color: Color) -> None:
        """
        Render a specific face.

        :param body: body that contain the face
        :type body: Body
        :param face: face to render
        :type face: tuple[int, int, int]
        :param normal: normal of the face
        :type normal: Vec3
        :param color: RGB color of the face
        :type color: Color
        """

        if (point1 := self.computed[face[0]]) is None:
            point1 = self.to_view_space(body.v[face[0]])
            point1 = self.project_point(point1)
            self.computed[face[0]] = point1

        if (point2 := self.computed[face[1]]) is None:
            point2 = self.to_view_space(body.v[face[1]])
            point2 = self.project_point(point2)
            self.computed[face[1]] = point2

        if (point3 := self.computed[face[2]]) is None:
            point3 = self.to_view_space(body.v[face[2]])
            point3 = self.project_point(point3)
            self.computed[face[2]] = point3

        p1x, p1y, p1z = point1
        p2x, p2y, p2z = point2
        p3x, p3y, p3z = point3

        if (p1x > self.camera.w and
            p2x > self.camera.w and
            p3x > self.camera.w):
            return

        if (p1x < 0 and
            p2x < 0 and
            p3x < 0):
            return

        if (p1y > self.camera.h and
            p2y > self.camera.h and
            p3y > self.camera.h):
            return

        if (p1y < 0 and
            p2y < 0 and
            p3y < 0):
            return

        if (p1z < self.camera.znear or
            p2z < self.camera.znear or
            p3z < self.camera.znear):
            return

        if (p1z > self.camera.zfar or
            p2z > self.camera.zfar or
            p3z > self.camera.zfar):
            return

        light_intensity = (normal * self.scene.light) / 2 + 0.5

        draw_triangle(
            self.buffer_ptr, *self.buffer.strides,
            self.depth_ptr, *self.depth.strides,
            p1x, p1y, p1z,
            p2x, p2y, p2z,
            p3x, p3y, p3z,
            *darken_color(color, light_intensity),
            self.camera.w, self.camera.h
        )

        self.triangles += 1

    def resize(self) -> None:
        """
        Regenerate screen and depth buffer when resizing the window.
        Should always be used after when the event ``pygame.VIDEORESIZE`` occurs.
        """

        self.buffer = pygame.surfarray.array3d(self.screen)
        self.depth = np.ones((self.buffer.shape[0],
                              self.buffer.shape[1]),
                              dtype=np.float32) * self.camera.zfar
        self.buffer.flags.writeable = True
        self.depth.flags.writeable = True
        self.buffer_ptr = self.buffer.__array_interface__['data'][0]
        self.depth_ptr = self.depth.__array_interface__['data'][0]
