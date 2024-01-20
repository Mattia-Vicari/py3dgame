import pygame
import cProfile
import py3dgame as p3g


def render_sphere():
    """
    Profile the rendering of a sphere with  quality 5.
    """

    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    clock = pygame.time.Clock()

    scene = p3g.Scene(p3g.color.BLACK, light=p3g.Vec3(0, - 1, - 1).normalize())
    sphere = p3g.Body.sphere("sphere", 1, pos=p3g.Vec3(0, 0, 0), quality=5)
    scene.add_body(sphere)
    camera = p3g.Camera(p3g.Vec3(-3, 0, 0), p3g.Vec3(1, 0, 0))
    renderer = p3g.Renderer(screen, camera, scene, clock)
    cProfile.runctx("renderer.render()", None, locals(), sort=1)

    pygame.quit()

if __name__ == "__main__":
    render_sphere()