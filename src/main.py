import pygame
from game import Ground, Player, Obstacle

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

obstacles = []
for i in range(2):
    obstacle = Obstacle(win_width, win_height)
    obstacles.append(obstacle)

delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.hold_jump()

    ground.update(game_speed, delta_time)
    player.update(delta_time)
    for obstacle in obstacles:
        obstacle.update(game_speed, delta_time)
        if player.rect.colliderect(obstacle.rect):
            print("game over")

    window.fill("white")
    ground.draw(window)
    player.draw(window)
    for obstacle in obstacles:
        obstacle.draw(window)

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()