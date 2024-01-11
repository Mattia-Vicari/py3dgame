import py3dgame as p3g
import pygame

width, height = 800, 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.SysFont('arial', 18, True)

    color = (
        p3g.Color.red,
        p3g.Color.green,
        p3g.Color.blue,
        p3g.Color.purple,
        p3g.Color.yellow,
        p3g.Color.cyan
    )

    scene = p3g.Scene(p3g.Color.black)
    scene.add_body(p3g.Body.cube(10, color=color))
    camera = p3g.Camera(p3g.Vec3(-50, 0, 15), p3g.Vec3(1, 0, -0.3))

    run = True
    while run:
        clock.tick(fps)
        real_fps = clock.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        scene.bodies[0].rotate_deg(1)

        p3g.render(screen, scene, camera, real_fps, font)

    pygame.quit()

if __name__ == "__main__":
    main()