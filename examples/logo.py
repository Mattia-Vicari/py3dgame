import py3dgame as p3g
import pygame
import math

width, height = 1080, 720

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 60

    color = (
        p3g.color.RED,
        p3g.color.GREEN,
        p3g.color.BLUE,
        p3g.color.PURPLE,
        p3g.color.YELLOW,
        p3g.color.CYAN
    )

    scene = p3g.Scene(p3g.color.BLACK, light=p3g.Vec3(0, 1, 0).normalize())
    logo = p3g.Body.logo("logo", rot=p3g.Quat(0, p3g.Vec3(-1, -1, 1)))
    scene.add_body(logo)
    camera = p3g.Camera(p3g.Vec3(0, -30, 0), p3g.Vec3(0, 1, 0))
    renderer = p3g.Renderer(screen, camera, scene, clock)
    run = True

    t = 0
    step = 1 / 180 * math.pi

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        camera.handle_movements()

        if t < 120:
            logo.rotate_deg(1)
        elif t < 210:
            logo.relative_move(pos=p3g.Vec3(0, 0, 0), rot=p3g.Quat(step, p3g.Vec3(1, 0, 0)))
        elif t < 300:
            logo.relative_move(pos=p3g.Vec3(0, 0, 0), rot=p3g.Quat(step, p3g.Vec3(0, 0, -1)))
        else:
            t = 0
            logo.rot = p3g.Quat(0, p3g.Vec3(-1, -1, 1))

        t += 1

        renderer.render()

    pygame.quit()

if __name__ == "__main__":
    main()