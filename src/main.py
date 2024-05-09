import os
import random
import pygame

def load_image(path):
    if not os.path.exists(path):
        print(f"{path} not found.")
        pygame.quit()
        exit(1)
    return pygame.image.load(path)

class Ground:
    def __init__(self, win_width, win_height):
        self.sprite = load_image("assets/ground.png")

        width = self.sprite.get_width()
        height = self.sprite.get_height()
        self.rects = [
            # At the bottom left of the window
            pygame.Rect(0, win_height - height, width, height),
            # Immediately after the first rect, off the screen
            # at the bottom right
            pygame.Rect(width - win_width, win_height - height, width, height)
        ]
        self.win_width = win_width

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
                self.rects[i].x = self.rects[i].width - self.win_width

    def draw(self, canvas):
        for rect in self.rects:
            canvas.blit(self.sprite, rect)

class Player:
    def __init__(self, ground_y):
        self.sprite = load_image("assets/dino/jump.png")

        self.rect = self.sprite.get_rect()
        self.rect.y = ground_y - self.sprite.get_height()
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

class Obstacle:
    def __init__(self, win_width, ground_y):
        # Default values
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.sprite = pygame.Surface((0, 0))

        self.speed = 100
        self.ground = ground_y
        self.win_width = win_width

        self.possible_sprites = []
        folder = "assets/cacti"
        for file in os.listdir(folder):
            image = load_image(f"{folder}/{file}")
            self.possible_sprites.append(image)

        self.spawn()

    # Randomly choose a sprite and offset position
    def spawn(self):
        self.sprite = random.choice(self.possible_sprites)
        self.sprite.set_colorkey((0, 0, 0)) # make the background transparent

        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()

        # The start is random so we don't generate
        # a sequence of random numbers that are close to each other
        start = random.randint(50, 200)
        offset = random.randint(start, 800)
        self.rect.x = self.win_width + offset
        self.rect.y = self.ground - self.rect.height

    def update(self, delta_time):
        self.rect.x -= self.speed * delta_time

        off_the_screen = self.rect.x < -self.rect.width
        if off_the_screen:
            self.spawn()

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

win_width = 600
win_height = 600
pygame.init()
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino")

clock = pygame.time.Clock()
fps = 60

ground = Ground(win_width, win_height)
player = Player(win_height)

obstacles = []
for i in range(2):
    obstacles.append(Obstacle(win_width, win_height))

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