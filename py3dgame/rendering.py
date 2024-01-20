"""
Module for handling the rendering pipeline.
"""

import heapq
import pygame
from .math3d import Vec3, Quat, Mat, rotate
from .color import WHITE, darken_color
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
            direction: Vec3 = Vec3(1, 0, 0),
            max_distance: int = 1000) -> None:

        self.pos = pos
        self.dir = direction
        self.zoom = 1000
        self.xs: Vec3 = (self.dir @ Vec3(0, 0, 1)).normalize()
        self.ys: Vec3 = (self.dir @ self.xs).normalize()
        self.mouse_pos = None
        self.top = Vec3(0, 0, 0)
        self.right = Vec3(0, 0, 0)
        self.bottom = Vec3(0, 0, 0)
        self.left = Vec3(0, 0, 0)
        self.k = self.dir * self.zoom * self.dir
        self.plane_center = self.pos + self.dir * self.zoom
        self.max_distance = max_distance

    def handle_movements(self) -> None:
        """
        Move the mare position with A, W, S, D or the arrows and the
        change the rotation using the mouse.
        """

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pos = self.pos - self.xs

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pos = self.pos + self.xs

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pos = self.pos + self.dir

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pos = self.pos - self.dir

        if mouse_buttons[1]:
            if self.mouse_pos is not None:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = Vec3(mouse_pos[0], mouse_pos[1], 0)
                angle = - (self.mouse_pos - mouse_pos).x / 1000
                self.dir = rotate(self.dir, Quat(angle, self.ys))
                self.xs = (self.dir @ Vec3(0, 0, 1)).normalize()
                self.ys = (self.dir @ self.xs).normalize()

                angle = (self.mouse_pos - mouse_pos).y / 1000
                self.dir = rotate(self.dir, Quat(angle, self.xs))
                self.xs = (self.dir @ Vec3(0, 0, 1)).normalize()
                self.ys = (self.dir @ self.xs).normalize()

                self.k = self.dir * self.zoom * self.dir

            mouse_pos = pygame.mouse.get_pos()
            self.mouse_pos = Vec3(mouse_pos[0], mouse_pos[1], 0)
        else:
            self.mouse_pos = None

        self.plane_center = self.pos + self.dir * self.zoom

    def update_fov(self, screen: pygame.Surface) -> None:
        """
        Computes the vectors to check whether a point is inside the field of view.

        :param screen: pygame active window
        :type screen: pygame.Surface
        """

        w = screen.get_width() / 2
        h = screen.get_height() / 2

        top_left = Vec3(- w, - h, self.zoom)
        top_right = Vec3(w, - h, self.zoom)
        bottom_right = Vec3(w, h, self.zoom)
        bottom_left = Vec3(- w, h, self.zoom)

        mat = Mat(self.xs, self.ys, self.dir).inverse()

        top_left = mat @ top_left
        top_right = mat @ top_right
        bottom_right = mat @ bottom_right
        bottom_left = mat @ bottom_left

        self.top = (top_left @ top_right).normalize()
        self.right = (top_right @ bottom_right).normalize()
        self.bottom = (bottom_right @ bottom_left).normalize()
        self.left = (bottom_left @ top_left).normalize()

    def inside_fov(self, *args: Vec3) -> bool:
        """
        Check whether a face is inside the field of view.

        :return: ``True`` if at least one vertex is inside the field of view,
            ``False`` otherwise
        :rtype: bool
        """

        for vertex in args:
            cam_to_vertex = vertex - self.pos

            if (self.top * cam_to_vertex > 0 and
                self.right * cam_to_vertex > 0 and
                self.bottom * cam_to_vertex > 0 and
                self.left * cam_to_vertex > 0):

                return True

        return False


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
        # TODO call this function only if the camera pos or dir changes
        self.camera.update_fov(self.screen)

        for body in self.scene.bodies.values():
            self.render_body(body)

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
                if self.camera.inside_fov(body.v[body.f[i][0]],
                                          body.v[body.f[i][1]],
                                          body.v[body.f[i][2]]):
                    self.triangles += 1
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

        distance = - (abs(cam_to_v1) + abs(cam_to_v2) + abs(cam_to_v3)) / 3

        if distance < - self.camera.max_distance:
            return False

        proj1 = self.camera.pos + cam_to_v1 * (self.camera.k / (cam_to_v1 * self.camera.dir))
        proj2 = self.camera.pos + cam_to_v2 * (self.camera.k / (cam_to_v2 * self.camera.dir))
        proj3 = self.camera.pos + cam_to_v3 * (self.camera.k / (cam_to_v3 * self.camera.dir))

        points = (
            self.world_to_screen(proj1),
            self.world_to_screen(proj2),
            self.world_to_screen(proj3),
        )

        light_intensity = (body.n[i] * self.scene.light) / 2 + 0.5

        if body.single_color:
            heapq.heappush(self.queue,
                           (distance, darken_color(body.color, light_intensity), points))
        else:
            heapq.heappush(self.queue,
                           (distance, darken_color(body.color[i], light_intensity), points))

    def world_to_screen(self, point: Vec3) -> tuple[int, int]:
        """
        Convert the 3d point projected on the camera plane
        in screen coordinates.

        :param point: 3d point to convert
        :type point: Vec3
        :return: new screen coordinates
        :rtype: tuple[int, int]
        """

        point = point - self.camera.plane_center
        x = self.camera.xs * point + self.screen.get_width() / 2
        y = self.camera.ys * point + self.screen.get_height() / 2

        return (x, y)
