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
        self.sprite = load_image("assets/imgs/ground.png")

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
        self.frame = 0
        self.previous_time = pygame.time.get_ticks()
        self.sprites = [load_image(path) for path in image_paths]
        self.masks = [pygame.mask.from_surface(sprite) for sprite in self.sprites]
        self.speed = animation_speed

    def current_sprite(self):
        return self.sprites[self.frame]

    def current_mask(self):
        return self.masks[self.frame]

    def animate(self):
        if self.speed <= 0: return # No animation

        max_index = len(self.sprites)
        time = pygame.time.get_ticks()

        # Switch through the different animation sprites every few miliseconds
        if time - self.previous_time > self.speed:
            self.frame += 1
            if self.frame == max_index:
                self.frame = 0
            self.previous_time = time


class Player:
    def __init__(self, ground_y):
        self.run_animation = Animation([
            "assets/imgs/run1.png",
            "assets/imgs/run2.png",
        ], 75)
        self.jump_animation = Animation(["assets/imgs/jump.png"], 0)
        self.rect = pygame.Rect(50, 0, 0, 0)
        self.animation = None
        self.point_effect = pygame.mixer.Sound("assets/sfx/point.wav")

        self.jumping = False
        self.acceleration = 50
        self.jump_speed = 100
        self.default_velocity = 600
        self.velocity = self.default_velocity
        self.ground_y = ground_y
        self.max_height = ground_y - 100

        self.score = 0
        self.high_score = 0
        self.interval = 10
        self.increment_interval = 0

    def hold_jump(self):
        if self.velocity + self.jump_speed < 900 and self.rect.y > 400:
            self.jumping = True
            # Increase jump height based on how long the jump is held
            self.velocity += self.jump_speed

    def jump(self, delta_time):
        self.velocity -= self.acceleration
        self.rect.y -= self.velocity * delta_time

        # If we're on or below the ground
        if self.rect.y >= self.ground_y - self.rect.height:
            self.rect.y = self.ground_y - self.rect.height
            self.velocity = self.default_velocity
            self.jumping = False

    # Return True if pixel perfect collision detected
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if obstacle.rect.x < self.rect.x:
                continue # Ignore obstacles behind us

            mask = obstacle.possible_masks[obstacle.index]
            our_mask = self.animation.current_mask()
            offset = (obstacle.rect.x - self.rect.x, obstacle.rect.y - self.rect.y)
            if our_mask.overlap(mask, offset):
                return True
        return False

    def reset(self):
        self.score = 0
        self.jumping = False
        self.rect.y = self.ground_y - self.rect.height

    def draw_score(self, canvas, font):
        high_score = font.render(f"HI {self.high_score}", False, (50, 50, 50))
        score = font.render(f"{int(self.score)}", False, (0, 0, 0))

        score_x = canvas.get_rect().w - score.get_width()
        high_score_x = score_x - high_score.get_width() - 20

        canvas.blit(score, (score_x, 0))
        canvas.blit(high_score, (high_score_x, 0))

    def draw(self, canvas, font):
        self.draw_score(canvas, font)

        sprite = self.animation.current_sprite()
        self.rect.width = sprite.get_width()
        self.rect.height = sprite.get_height()
        if self.rect.y == 0: # Hasn't been set yet
            self.rect.y = self.ground_y - self.rect.height
        canvas.blit(sprite, self.rect)

    def update(self, delta_time):
        if self.jumping:
            self.jump(delta_time)
            self.animation = self.jump_animation
        else:
            self.animation = self.run_animation
        self.animation.animate()

        # Increment the score every "interval" frames
        self.increment_interval += 1
        if self.increment_interval == self.interval:
            self.score += 1
            if self.score % 100 == 0:
                pygame.mixer.Sound.play(self.point_effect)
            self.increment_interval = 0

class Obstacle:
    def __init__(self, ground_y):
        self.ground = ground_y
        self.spawn_position = 0

        self.possible_sprites = []
        self.possible_masks = []
        self.index = 0
        folder = "assets/imgs"
        for file in os.listdir(folder):
            if "cacti" not in file:
                continue
            image = load_image(f"{folder}/{file}")
            mask = pygame.mask.from_surface(image)
            self.possible_sprites.append(image)
            self.possible_masks.append(mask)

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.sprite = pygame.Surface((0, 0))

    def spawn(self, start):
        self.index = random.randint(0, len(self.possible_sprites) - 1)
        self.sprite = self.possible_sprites[self.index]
        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()

        self.spawn_position = random.randint(start, start + 400)
        self.rect.x = self.spawn_position
        self.rect.y = self.ground - self.rect.height


class Obstacles:
    def __init__(self, window_width, ground_y):
        self.ground_y = ground_y
        self.obstacles = [Obstacle(ground_y) for _ in range(3)]
        self.min_obstacle_gap = 200
        self.window_width = window_width

    def reset(self):
        self.obstacles = [Obstacle(self.ground_y) for _ in range(3)]

    def update(self, speed, delta_time):
        for i in range(len(self.obstacles)):
            self.obstacles[i].rect.x -= speed * delta_time
            off_the_screen = self.obstacles[i].rect.x < -self.obstacles[i].rect.width
            if off_the_screen:
                prev_position = self.obstacles[i - 1].spawn_position
                prev_position += self.min_obstacle_gap

                start = prev_position if i > 0 else self.window_width
                self.obstacles[i].spawn(start)

    def draw(self, canvas):
        for obstacle in self.obstacles:
            canvas.blit(obstacle.sprite, obstacle.rect)

