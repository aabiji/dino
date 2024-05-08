import os
import random

def init_script():
    # Disable pygame import message
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

    # Assure that our required sprites are present
    spritesheet_path = "assets/spritesheet.png"
    if not os.path.exists(spritesheet_path):
        print("Game assets not found")
        exit()
init_script()

import pygame
pygame.init()

class Spritesheet:
    def __init__(self):
        path = "assets/spritesheet.png"
        self.sheet = pygame.image.load(path)
        self.width = self.sheet.get_width()
        self.height = self.sheet.get_height()

    # Return a portion of the spritesheet as a new sprite
    def crop(self, x, y, width, height):
        crop_area = pygame.Rect(x, y, width, height)
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), crop_area)
        return sprite

class Ground:
    def __init__(self, window_width, window_height, spritesheet):
        width = spritesheet.width
        height = 25

        self.sprite = spritesheet.crop(0, spritesheet.height - height, width, height)
        self.sprite.set_colorkey((0, 0, 0)) # Make the background transparent
        self.rects = [
            # At the bottom left of the window
            pygame.Rect(0, window_height - height, width, height),
            # Immediately after the first rect, off the screen
            # at the bottom right
            pygame.Rect(width - window_width, window_height - height, width, height)
        ]
        self.window_width = window_width

    def update(self):
        # We use 2 sprites moving to the left
        # to achieve smooth scrolling. When the first
        # sprite goes completely off the screen, the
        # second sprite replaces it and the first sprite goes
        # immediately after the second sprite. Vice versa.
        for i in range(2):
            self.rects[i].x -= 1

            # Move to the end of the other sprite when
            # the sprite moves completely off the screen
            if self.rects[i].x == -self.rects[i].width:
                self.rects[i].x = self.rects[i].width - self.window_width

    def draw(self, canvas):
        for rect in self.rects:
            canvas.blit(self.sprite, rect)

class Player:
    def __init__(self, ground_y, spritesheet):
        self.sprite = spritesheet.crop(1335, 0, 90, 95)
        self.sprite.set_colorkey((0, 0, 0)) # Make the background transparent

        self.rect = self.sprite.get_rect()
        self.rect.y = ground_y - 95
        self.rect.x = 50

        self.jumping_up = False
        self.jumping_down = False
        self.jump_extra = 0
        self.max_jump_height = ground_y - self.rect.height * 3

        self.gravity = 300
        self.ground = ground_y

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

    def hold_jump(self):
        if self.jumping_down:
            return
        self.jumping_up = True
        # Increase our jump height based on how long we jump
        self.jump_extra += 1

    def jump_up(self, delta_time):
        self.rect.y -= self.gravity * delta_time

        peek_height = self.max_jump_height - self.jump_extra
        if self.rect.y <= peek_height: # Reached the jump peek
            self.rect.y = self.max_jump_height
            self.jumping_up = False
            self.jumping_down = True
            self.jump_extra = 0

    def jump_down(self, delta_time):
        self.rect.y += self.gravity * delta_time

        base_height = self.ground - self.rect.height
        if self.rect.y >= base_height: # On the ground
            self.rect.y = base_height
            self.jumping_down = False

    def update(self, delta_time):
        if self.jumping_down:
            self.jump_down(delta_time)
        elif self.jumping_up:
            self.jump_up(delta_time)

PREVIOUS_OFFSET = 0 # TODO: remove this

class Obstacle:
    def __init__(self, window_width, ground_y, possible_sprites):
        # Default values
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.sprite = pygame.Surface((0, 0))

        self.speed = 100
        self.ground = ground_y
        self.possible_sprites = possible_sprites
        self.window_width = window_width

        self.spawn()

    # TODO: reimplement this
    # Choose a random offset that avoids being
    # to close to other obstacles
    def random_offset(self):
        global PREVIOUS_OFFSET
        offset = random.randint(50, 800)
        while abs(offset - PREVIOUS_OFFSET) < 300:
            offset = random.randint(50, 800)
        PREVIOUS_OFFSET = offset
        return offset

    # Randomly choose a sprite and offset position
    def spawn(self):
        self.sprite = random.choice(self.possible_sprites)
        self.sprite.set_colorkey((0, 0, 0)) # make the background transparent

        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()
        self.rect.x = self.window_width + self.random_offset()
        self.rect.y = self.ground - self.rect.height

    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time

        off_the_screen = self.rect.x < -self.rect.width
        if off_the_screen:
            self.spawn()

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

# TODO: refactor the rest
# TODO: idea: what if the spritesheet class was responsible for
# extracting the sprites?
fps = 60
window_width = 600
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()

sheet = Spritesheet()
ground = Ground(window_width, window_height, sheet)
player = Player(window_height, sheet)

obstacles = []
cacti_sprites = [
    sheet.crop(650, 0, 52, 100),
    sheet.crop(702, 0, 50, 100),
    sheet.crop(752, 0, 98, 100),
    sheet.crop(850, 0, 103, 100)
]
for i in range(2):
    obstacles.append(Obstacle(window_width,window_height, cacti_sprites))

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

    ground.update()
    player.update(delta_time)
    for obstacle in obstacles:
        obstacle.update(delta_time)
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
