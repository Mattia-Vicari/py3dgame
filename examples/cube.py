import py3dgame as p3g
import pygame

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

    scene = p3g.Scene(p3g.color.BLACK, light=p3g.Vec3(0, 1, -1).normalize())
    cube = p3g.Body.cube("cube", 10, color=color, pos=p3g.Vec3(0, 0, 0))
    scene.add_body(cube)
    camera = p3g.Camera(p3g.Vec3(-50, 0, 15), p3g.Vec3(1, 0, -0.3))
    renderer = p3g.Renderer(screen, camera, scene, clock)
    run = True

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        camera.handle_movements()
        cube.rotate_deg(1)
        renderer.render()

    pygame.quit()

if __name__ == "__main__":
    main()