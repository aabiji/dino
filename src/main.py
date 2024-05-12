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

class Animation:
    def __init__(self, image_paths):
        self.sprite_index = 0
        self.previous_time = pygame.time.get_ticks()
        self.sprites = [load_image(path) for path in image_paths]

    def current_sprite(self):
        return self.sprites[self.sprite_index]

    def animate(self):
        duration = 50
        max_index = len(self.sprites)
        time = pygame.time.get_ticks()

        # Switch through the different animation frames
        # (sprites) every speed miliseconds
        if time - self.previous_time > duration:
            self.sprite_index += 1
            if self.sprite_index == max_index:
                self.sprite_index = 0
            self.previous_time = time

class Player:
    def __init__(self, ground_y):
        run_image_paths = ["assets/dino/run1.png", "assets/dino/run2.png"]
        self.run_animation = Animation(run_image_paths)

        jump_image_paths = ["assets/dino/jump.png"]
        self.jump_animation = Animation(jump_image_paths)

        self.rect = pygame.Rect(50, 0, 0, 0)

        self.jumping = False
        self.default_velocity = 400
        self.base_velocity = self.default_velocity
        self.velocity = self.base_velocity
        self.acceleration = 10
        self.ground = ground_y

        self.score = 0

    def get_current_sprite(self):
        if self.jumping:
            return self.jump_animation.current_sprite()
        else:
            return self.run_animation.current_sprite()

    def hold_jump(self):
        if self.base_velocity < self.default_velocity + 100:
            player.jumping = True
            # Increase jump height based on
            # how long the jump is held
            self.base_velocity += 10
            self.velocity += 10

    def jump(self, delta_time):
        self.velocity -= self.acceleration
        self.rect.y -= self.velocity * delta_time

        below_ground = self.rect.y > self.ground - self.rect.height
        if self.velocity <= -self.base_velocity or below_ground:
            self.rect.y = self.ground - self.rect.height
            self.jumping = False
            self.base_velocity = self.default_velocity
            self.velocity = self.base_velocity

    def draw(self, canvas):
        sprite = self.get_current_sprite()

        self.rect.width = sprite.get_width()
        self.rect.height = sprite.get_height()
        if self.rect.y == 0: # Hasn't been set yet
            self.rect.y = self.ground - self.rect.height

        canvas.blit(sprite, self.rect)

    def update(self, delta_time):
        if self.jumping:
            self.jump(delta_time)
            self.jump_animation.animate()
        else:
            self.run_animation.animate()
        self.score += 1

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
        self.rect.y = self.ground - self.rect.height - 5

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