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
        p3g.color.RED,
        p3g.color.GREEN,
        p3g.color.BLUE,
        p3g.color.PURPLE,
        p3g.color.YELLOW,
        p3g.color.CYAN
    )

    scene = p3g.Scene(p3g.color.BLACK)
    scene.add_body(p3g.Body.cube("cube", 10, color=color))
    camera = p3g.Camera(p3g.Vec3(-50, 0, 15), p3g.Vec3(1, 0, -0.3))

    run = True
    while run:
        clock.tick(fps)
        real_fps = clock.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        scene.bodies["cube"].rotate_deg(1)

        p3g.render(screen, scene, camera, real_fps, font)

    pygame.quit()

if __name__ == "__main__":
    main()