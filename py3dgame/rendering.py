"""
Module for handling the rendering pipeline.
"""

import heapq
import pygame
from .math3d import Vec3
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

    def __init__(self, pos: Vec3 = Vec3(0, 0, 0), direction: Vec3 = Vec3(1, 0, 0)) -> None:

        self.pos = pos
        self.dir = direction
        self.zoom = 1000
        self.xs: Vec3 = self.dir @ Vec3(0, 0, 1)
        self.ys: Vec3 = self.dir @ self.xs

    # TODO add methods to move the camera


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

        pygame.display.set_caption(caption)

    def render(self) -> None:
        """
        Render all the object in scene.
        """

        self.screen.fill(self.scene.bgc)

        for body in self.scene.bodies.values():
            self.render_body(body)

        fps = self.clock.get_fps()
        text = self.font.render(f"FPS: {fps:.2f}", True, WHITE)
        self.screen.blit(text, (10, 10))

        while self.queue:
            _, color, points = heapq.heappop(self.queue)
            pygame.draw.polygon(self.screen, color, points)

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

    def render_face(self, body: Body, i: int) -> None:
        """
        Render a specific face.

        :param body: body that contain the face
        :type body: Body
        :param i: index of the face
        :type i: int
        """

        cam_to_v1 = body.v[body.f[i][0]] - self.camera.pos
        cam_to_v2 = body.v[body.f[i][1]] - self.camera.pos
        cam_to_v3 = body.v[body.f[i][2]] - self.camera.pos

        distance = - (abs(cam_to_v1) + abs(cam_to_v2) + abs(cam_to_v3))

        cam_to_v1.normalize()
        cam_to_v2.normalize()
        cam_to_v3.normalize()

        proj1 = self.camera.pos + cam_to_v1 * (self.camera.dir * self.camera.zoom *
                                               self.camera.dir / (cam_to_v1 * self.camera.dir))
        proj2 = self.camera.pos + cam_to_v2 * (self.camera.dir * self.camera.zoom *
                                               self.camera.dir / (cam_to_v2 * self.camera.dir))
        proj3 = self.camera.pos + cam_to_v3 * (self.camera.dir * self.camera.zoom *
                                               self.camera.dir / (cam_to_v3 * self.camera.dir))

        points = (
            self.world_to_screen(proj1),
            self.world_to_screen(proj2),
            self.world_to_screen(proj3),
        )

        light_intensity = (body.n[i] * self.scene.light) / 2 + 0.5

        if body.single_color:
            heapq.heappush(self.queue, (distance, darken_color(body.color, light_intensity), points))
        else:
            heapq.heappush(self.queue, (distance, darken_color(body.color[i], light_intensity), points))

    def world_to_screen(self, point: Vec3) -> tuple[int, int]:
        """
        Convert the 3d point projected on the camera plane
        in screen coordinates.

        :param point: 3d point to convert
        :type point: Vec3
        :return: new screen coordinates
        :rtype: tuple[int, int]
        """

        point = point - (self.camera.pos + self.camera.dir * self.camera.zoom)
        x = (Vec3(self.camera.xs.x, self.camera.xs.y, self.camera.xs.z) *
             point + self.screen.get_width() / 2)
        y = (Vec3(self.camera.ys.x, self.camera.ys.y, self.camera.ys.z) *
              point + self.screen.get_height() / 2)

        return (int(x), int(y))
