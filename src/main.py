import pygame
pygame.init()

fps = 60
window_size = (600, 600)
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

x = 0
size = 30
y = window_size[1] - size

delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    window.fill("black")

    size = 30
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(window, "green", rect)

    keys = pygame.key.get_pressed()
    height = 500 * delta_time
    if keys[pygame.K_SPACE]:
        print("jump!")
        y -= height

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()
