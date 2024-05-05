import pygame
pygame.init()

fps = 60
window_size = (600, 600)
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

size = 30
bottom_left = window_size[1] - size
x, y = 0, bottom_left
in_the_air = False
fall_rate = 300
jump_rate = 400
min_height = bottom_left - size * 2.5

delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    window.fill("black")

    keys = pygame.key.get_pressed()
    pressed_space = keys[pygame.K_SPACE]
    if pressed_space and y > min_height:
        in_the_air = True
        y -= jump_rate * delta_time

    if in_the_air and not pressed_space:
        y += fall_rate * delta_time
        if y >= bottom_left:
            y = bottom_left
            in_the_air = False

    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(window, "green", rect)

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()
