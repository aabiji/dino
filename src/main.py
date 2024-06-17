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
    def __init__(self, win_height):
        self.sprite = load_image("assets/ground.png")

        width = self.sprite.get_width()
        height = self.sprite.get_height()
        self.rects = [
            # At the bottom left of the window
            pygame.Rect(0, win_height - height, width, height),
            # Immediately after the first rect, off the screen
            # at the bottom right
            pygame.Rect(width, win_height - height, width, height)
        ]

    def update(self, speed, delta_time):
        # We use 2 sprites moving to the left in unison
        # to achieve smooth scrolling. When the first
        # sprite goes completely off the screen, the
        # second sprite is already at the start so
        # replaces the first sprite and the first sprite goes
        # immediately after the second sprite. Vice versa.
        for i in range(2):
            self.rects[i].x -= speed * delta_time

            # Move to the end of the other sprite when
            # the sprite moves completely off the screen
            if self.rects[i].x <= -self.rects[i].width:
                self.rects[i].x = self.rects[i].width

    def draw(self, canvas):
        for rect in self.rects:
            canvas.blit(self.sprite, rect)

class Animation:
    def __init__(self, image_paths, animation_speed):
        self.sprite_index = 0
        self.previous_time = pygame.time.get_ticks()
        self.sprites = [load_image(path) for path in image_paths]
        self.speed = animation_speed

    def current_sprite(self):
        return self.sprites[self.sprite_index]

    def animate(self):
        max_index = len(self.sprites)
        time = pygame.time.get_ticks()

        # Switch through the different animation sprites every few miliseconds
        if time - self.previous_time > self.speed:
            self.sprite_index += 1
            if self.sprite_index == max_index:
                self.sprite_index = 0
            self.previous_time = time

class Player:
    def __init__(self, ground_y):
        self.run_animation = Animation([
            "assets/dino/run1.png",
            "assets/dino/run2.png",
        ], 75)
        self.jump_animation = Animation(["assets/dino/jump.png"], 0)

        self.rect = pygame.Rect(50, 0, 0, 0)

        self.jumping = False
        self.acceleration = 50
        self.jump_speed = self.acceleration * 10
        self.default_velocity = 600
        self.velocity = self.default_velocity
        self.ground_y = ground_y
        self.max_height = ground_y - 100

        self.score = 0

    # FIXME: this isn't entirely correct
    def hold_jump(self):
        if self.rect.y >= self.max_height:
            self.jumping = True
            # Increase jump height based on
            # how long the jump is held
            self.velocity += self.jump_speed

    def jump(self, delta_time):
        self.velocity -= self.acceleration
        self.rect.y -= self.velocity * delta_time

        # If we're on or below the ground
        if self.rect.y >= self.ground_y - self.rect.height:
            self.rect.y = self.ground_y - self.rect.height
            self.velocity = self.default_velocity
            self.jumping = False

    def get_current_sprite(self):
        if self.jumping:
            return self.jump_animation.current_sprite()
        else:
            return self.run_animation.current_sprite()

    def draw(self, canvas):
        sprite = self.get_current_sprite()
        self.rect.width = sprite.get_width()
        self.rect.height = sprite.get_height()
        if self.rect.y == 0: # Hasn't been set yet
            self.rect.y = self.ground_y - self.rect.height
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
        #self.sprite.set_colorkey((0, 0, 0)) # make the background transparent

        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()

        # The start is random so we don't generate
        # a sequence of random numbers that are close to each other
        start = random.randint(50, 200)
        offset = random.randint(start, 800)
        self.rect.x = self.win_width + offset
        self.rect.y = self.ground - self.rect.height - 5

    def update(self, speed, delta_time):
        self.rect.x -= speed * delta_time

        off_the_screen = self.rect.x < -self.rect.width
        if off_the_screen:
            self.spawn()

    def draw(self, canvas):
        canvas.blit(self.sprite, self.rect)

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
    obstacles.append(Obstacle(win_width, win_height))

path = "assets/PressStart2P-Regular.ttf"
font = pygame.font.Font(path, 15)
max_score = 0

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

    high_score = font.render(f"HI {max_score}", False, (50, 50, 50))
    score = font.render(f"{player.score}", False, (0, 0, 0))
    score_x = win_width - score.get_width()
    high_score_x = score_x - high_score.get_width() - 20
    window.blit(score, (score_x, 0))
    window.blit(high_score, (high_score_x, 0))

    pygame.display.update()

    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()