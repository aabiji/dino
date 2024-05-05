import pygame
pygame.init()

fps = 60
window_size = (600, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("dino")
clock = pygame.time.Clock()

size = 30
bottom_left = window_size[1] - size
x, y = 0, bottom_left
jumping = False
default_velocity = 2000
velocity = default_velocity
acceleration = 0.01
jumping = False
min_height = bottom_left - size * 4.5

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
        velocity += acceleration
        y -= velocity * delta_time
        jumping = True

    if jumping and not pressed_space:
        velocity -= acceleration
        y += abs(velocity) * delta_time
        if y > bottom_left:
            velocity = default_velocity
            y = bottom_left
            jumping = False

    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(window, "green", rect)

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()
