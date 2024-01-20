"""
Module for handling the rendering pipeline.
"""

import math
import heapq
import pygame
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

    def handle_movements(self) -> None:
        """
        Move the mare position with A, W, S, D or the arrows and the
        change the rotation using the mouse.
        """

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos = self.pos - self.right

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos = self.pos + self.right

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos = self.pos + self.dir

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos = self.pos - self.dir

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
        self.clock = clock
        self.queue = []
        self.triangles = 0

        pygame.display.set_caption(caption)

    def render(self) -> None:
        """
        Render all the object in scene.
        """

        self.screen.fill(self.scene.bgc)
        self.triangles = 0
        self.camera.update_projection_space(self.screen)
        self.camera.update_view_space()
        # self.buffer = pygame.surfarray.pixels3d(self.screen)
        # self.depth = np.zeros((self.buffer.shape[0], self.buffer.shape[1]))

        for body in self.scene.bodies.values():
            self.render_body(body)

        # del self.buffer

        while self.queue:
            _, color, points = heapq.heappop(self.queue)
            pygame.draw.polygon(self.screen, color, points)

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

        point1 = self.to_view_space(body.v[body.f[i][0]])
        point2 = self.to_view_space(body.v[body.f[i][1]])
        point3 = self.to_view_space(body.v[body.f[i][2]])

        point1 = self.project_point(point1)
        point2 = self.project_point(point2)
        point3 = self.project_point(point3)

        if (point1[0] > 1 and point2[0] > 1 and point3[0] > 1):
            return None

        if (point1[0] < - 1 and point2[0] < - 1 and point3[0] < - 1):
            return None

        if (point1[1] > 1 and point2[1] > 1 and point3[1] > 1):
            return None

        if (point1[1] < - 1 and point2[1] < - 1 and point3[1] < - 1):
            return None

        distance = - (point1[2] + point2[2] + point3[2])

        if (point1[2] < self.camera.znear and
            point2[2] < self.camera.znear and
            point3[2] < self.camera.znear):
            return None

        points = (
            ((point1[0] + 1) / 2 * self.camera.w, (- point1[1] + 1) / 2 * self.camera.h),
            ((point2[0] + 1) / 2 * self.camera.w, (- point2[1] + 1) / 2 * self.camera.h),
            ((point3[0] + 1) / 2 * self.camera.w, (- point3[1] + 1) / 2 * self.camera.h)
        )

        light_intensity = (body.n[i] * self.scene.light) / 2 + 0.5

        if body.single_color:
            heapq.heappush(self.queue,
                           (distance, darken_color(body.color, light_intensity), points))
            # self.draw_triangle(points[0], points[1], points[2],
            #                    darken_color(body.color, light_intensity))
        else:
            heapq.heappush(self.queue,
                           (distance, darken_color(body.color[i], light_intensity), points))
            # self.draw_triangle(points[0], points[1], points[2],
            #                    darken_color(body.color[i], light_intensity))

        self.triangles += 1

        return None

    def draw_triangle(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
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

        p1x = int(p1[0])
        p1y = int(p1[1])
        p2x = int(p2[0])
        p2y = int(p2[1])
        p3x = int(p3[0])
        p3y = int(p3[1])
        first_row = max(min(p1y, p2y, p3y), 0)
        last_row = min(max(p1y, p2y, p3y), self.camera.h)
        first_col = max(min(p1x, p2x, p3x), 0)
        last_col = min(max(p1x, p2x, p3x), self.camera.w)

        for y in range(first_row, last_row + 1):
            for x in range(first_col, last_col + 1):
                s1 = (x - p2x) * (p1y - p2y) - (p1x - p2x) * (y - p2y)
                s2 = (x - p3x) * (p2y - p3y) - (p2x - p3x) * (y - p3y)
                s3 = (x - p1x) * (p3y - p1y) - (p3x - p1x) * (y - p1y)

                if (s1 >= 0) == (s2 >= 0) == (s3 >= 0):
                    self.buffer[x, y, 0] = color[0]
                    self.buffer[x, y, 1] = color[1]
                    self.buffer[x, y, 2] = color[2]
