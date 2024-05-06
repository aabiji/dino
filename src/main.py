import pygame
import random
pygame.init()

fps = 60
window_size = (600, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("dino")
clock = pygame.time.Clock()

size = 30
ground_y = window_size[1] - size
default_jump_peek = ground_y - size * 4
jump_peek = default_jump_peek
dino = pygame.Rect(50, ground_y, size, size)

going_up = False
up_force = 400
going_down = False
down_force = 300

speed = 100
PREVIOUS_OFFSET = 0


class Obstacle:
    def __init__(self):
        size = 10
        x = window_size[0] + self.random_offset()
        y = window_size[1] - size
        self.rect = pygame.Rect(x, y, size, size)

    # Choose a random offset that avoids being
    # to close to other obstacles
    def random_offset(self):
        global PREVIOUS_OFFSET
        offset = random.randint(50, 500)
        while abs(offset - PREVIOUS_OFFSET) < 100:
            offset = random.randint(50, 500)
        PREVIOUS_OFFSET = offset
        return offset

    def update(self, speed):
        self.rect.x -= speed * delta_time
        if self.rect.x < 0:
            self.rect.x = window_size[0] + self.random_offset()

    def draw(self):
        pygame.draw.circle(window, "red", (self.rect.x,
                           self.rect.y), self.rect.width)


obstacles = [Obstacle(), Obstacle()]

delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not going_down:
        going_up = True
        # Jump a little higher based on how long we hold the space key
        jump_peek -= 1

    if going_down:
        dino.y += down_force * delta_time
        if dino.y > ground_y:
            dino.y = ground_y
            going_down = False
    elif going_up:
        dino.y -= up_force * delta_time
        if dino.y < jump_peek:
            dino.y = jump_peek
            going_up = False
            going_down = True
            jump_peek = default_jump_peek

    for obstacle in obstacles:
        obstacle.update(speed)
        if dino.colliderect(obstacle.rect):
            print("game over")

    window.fill("black")

    pygame.draw.rect(window, "green", dino)

    for obstacle in obstacles:
        obstacle.draw()

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()
