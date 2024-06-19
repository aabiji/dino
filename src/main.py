import pygame
from game import Ground, Player, Obstacles

# TODO: High score
# TODO: game over
# TODO: mediapipe integration
# TODO: install model automatically if we haven't already

win_width = 600
win_height = 500
pygame.init()
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino")

clock = pygame.time.Clock()
fps = 60
game_speed = 300

ground = Ground(win_height)
player = Player(win_height)
obstacle_manager = Obstacles(win_width, win_height)

delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.hold_jump()
    if keys[pygame.K_q]:
        running = False

    ground.update(game_speed, delta_time)
    player.update(delta_time, obstacle_manager.obstacles)
    obstacle_manager.update(game_speed, delta_time)

    window.fill("white")
    ground.draw(window)
    player.draw(window)
    obstacle_manager.draw(window)

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()