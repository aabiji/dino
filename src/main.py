# TODO: the code's really messy. please refactor
# TODO: add animations
# TODO: be able to choose small cacti as well
# TODO: when we jump it feels like we're hitting a ceiling. why?

import pygame
import random
pygame.init()

fps = 60
window_width = 600
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("dino")
clock = pygame.time.Clock()

PREVIOUS_OFFSET = 0

def crop_spritesheet(x, y, width, height):
    sheet = pygame.image.load("sprite.png")
    crop_area = pygame.Rect(x, y, width, height)
    sprite = pygame.Surface((width, height))
    sprite.blit(sheet, (0, 0), crop_area)
    return sprite

class Ground:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.rect = pygame.Rect(0, window_height - 25, 2404, 25)
        self.sprite = crop_spritesheet(0, 105, 2404, 25)

    def update(self):
        # Shift the sprite across the viewport until we get to the last bit
        self.rect.x -= 1
        max_scroll = self.sprite.get_width() - self.window_width
        if abs(self.rect.x) == max_scroll:
            self.rect.x = 0

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

class Player:
    def __init__(self, ground_y):
        self.ground = ground_y
        self.rect = pygame.Rect(50, self.ground, 30, 30)
        self.jump_peek = self.ground - self.rect.height * 10
        self.jumping_up = False
        self.jumping_down = False
        self.jump_extra = 0
        self.gravity = 300

        self.sprite = crop_spritesheet(1335, 0, 90, 95)
        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()
        self.rect.y = self.ground - self.rect.height
        self.sprite.set_colorkey((0, 0, 0)) # make background transparent

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

    def jump(self):
        if self.jumping_down:
            return

        self.jumping_up = True
        # Increase our jump height based on how
        # long we jump
        self.jump_extra += 1

    def update(self, delta_time):
        # Move up or down a little bit each frame
        if self.jumping_down:
            self.rect.y += self.gravity * delta_time
            below_ground = self.rect.y >= self.ground - self.rect.height
            if below_ground:
                self.rect.y = self.ground - self.rect.height
                self.jumping_down = False

        if self.jumping_up:
            self.rect.y -= self.gravity * delta_time
            too_high = self.rect.y < self.jump_peek - self.jump_extra
            if too_high:
                self.rect.y = self.jump_peek
                self.jumping_up = False
                self.jumping_down = True
                self.jump_extra = 0

cacti_sprites = [
    crop_spritesheet(650, 0, 52, 100),
    crop_spritesheet(702, 0, 50, 100),
    crop_spritesheet(752, 0, 98, 100),
    crop_spritesheet(850, 0, 103, 100)
]

class Obstacle:
    def __init__(self, window_width, ground_y):
        self.width = window_width
        self.speed = 100
        self.sprite = None
        self.ground = ground_y
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.spawn()

    # Choose a random offset that avoids being
    # to close to other obstacles
    def random_offset(self):
        global PREVIOUS_OFFSET
        offset = random.randint(50, 800)
        while abs(offset - PREVIOUS_OFFSET) < 300:
            offset = random.randint(50, 800)
        PREVIOUS_OFFSET = offset
        return offset

    def spawn(self):
        self.rect.x = self.width + self.random_offset()
        self.sprite = random.choice(cacti_sprites)
        self.sprite.set_colorkey((0, 0, 0)) # make background transparent
        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()
        self.rect.y = self.ground - self.rect.height

    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time
        if self.rect.x < -self.sprite.get_width(): # off the screen
            self.spawn()

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

ground = Ground(window_width, window_height)
player = Player(window_height)
obstacles = []
for i in range(2):
    obstacles.append(Obstacle(window_width,window_height))

delta_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.jump()

    ground.update()
    player.update(delta_time)
    for obstacle in obstacles:
        obstacle.update(delta_time)
        if player.rect.colliderect(obstacle.rect):
            print("game over")

    window.fill("black")
    ground.draw(window)
    player.draw(window)
    for obstacle in obstacles:
        obstacle.draw(window)

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()