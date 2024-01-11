from .math3d import Vec3
from .color import Color, invert_color
from .scene import Scene, Body
import pygame

class Camera:
    def __init__(self, pos: Vec3 = Vec3(0, 0, 0), dir: Vec3 = Vec3(1, 0, 0)) -> None:
        self.pos = pos
        self.dir = dir
        self.zoom = 1000
        self.xs: Vec3 = self.dir @ Vec3(0, 0, 1)
        self.ys: Vec3 = self.dir @ self.xs


def world_to_screen(point: Vec3, camera: Camera):
    point = point - (camera.pos + camera.dir * camera.zoom)
    x = Vec3(camera.xs.x, camera.xs.y, camera.xs.z) * point + 400
    y = Vec3(camera.ys.x, camera.ys.y, camera.ys.z) * point + 300

    return (int(x), int(y))


def render_face(screen: pygame.Surface, body: Body, i: int, camera: Camera):
    cam_to_v1 = (body.v[body.f[i][0]] - camera.pos).normalize()
    cam_to_v2 = (body.v[body.f[i][1]] - camera.pos).normalize()
    cam_to_v3 = (body.v[body.f[i][2]] - camera.pos).normalize()

    proj1 = camera.pos + cam_to_v1 * (camera.dir * camera.zoom * camera.dir / (cam_to_v1 * camera.dir))
    proj2 = camera.pos + cam_to_v2 * (camera.dir * camera.zoom * camera.dir / (cam_to_v2 * camera.dir))
    proj3 = camera.pos + cam_to_v3 * (camera.dir * camera.zoom * camera.dir / (cam_to_v3 * camera.dir))

    points = (
        world_to_screen(proj1, camera),
        world_to_screen(proj2, camera),
        world_to_screen(proj3, camera),
    )

    if body.single_color:
        pygame.draw.polygon(screen, body.color, points)
    else:
        pygame.draw.polygon(screen, body.color[i], points)
        #pygame.draw.lines(screen, invert_color(body.color[i]), True, points, 3)




def render_body(screen: pygame.Surface, body: Body, camera: Camera):
    for i, normal in enumerate(body.n):
        cam_to_vertex = body.v[body.f[i][0]] - camera.pos

        if cam_to_vertex * normal > 0:
            render_face(screen, body, i, camera)


def render(screen: pygame.Surface, scene: Scene, camera: Camera, real_fps: float = None, font: pygame.font.Font = None):
    screen.fill(scene.bgc)

    if real_fps is not None:
        text = font.render(f"FPS: {real_fps:.2f}", True, Color.white)
        screen.blit(text, (10, 10))

    for body in scene.bodies:
        render_body(screen, body, camera)

    pygame.display.flip()
