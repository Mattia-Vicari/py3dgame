import py3dgame as p3g
import pygame

width, height = 1080, 720

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 1000

    scene = p3g.Scene(p3g.color.BLACK, light=p3g.Vec3(0, 1, 0).normalize())
    coin = p3g.Body.from_obj("assets/coin.obj", "coin")
    scene.add_body(coin)
    camera = p3g.Camera(p3g.Vec3(-3, 0, 1), p3g.Vec3(1, 0, -0.3))
    renderer = p3g.Renderer(screen, camera, scene, clock)
    run = True

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        camera.handle_movements(clock.get_fps())
        coin.rotate_deg(1)
        renderer.render()

    pygame.quit()

if __name__ == "__main__":
    main()