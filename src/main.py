# TODO: improve performance
# TODO: don't immediately restart game
# TODO: birds and clouds
# TODO: segfault??
# TODO: show hands better

import cv2
import pygame
import hands
from game import Ground, Player, Obstacles

pygame.init()

win_width = 600
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino")
game_surface = pygame.Surface((win_width, win_height))
menu_surface = pygame.Surface((win_width, win_height))

font_path = "assets/PressStart2P-Regular.ttf"
text_font = pygame.font.Font(font_path, 15)
msg_font = pygame.font.Font(font_path, 20)
game_over_message1 = msg_font.render("Game over", False, (0, 0, 0))
game_over_message2 = msg_font.render("Press Space to restart", False, (0, 0, 0))

jump_sound = pygame.mixer.Sound("assets/sfx/jump.wav")
die_sound = pygame.mixer.Sound("assets/sfx/die.wav")

clock = pygame.time.Clock()
fps = 60
game_speed = 300

ground = Ground(win_height)
player = Player(win_height)
obstacle_manager = Obstacles(win_width, win_height)
game_over = False

video = cv2.VideoCapture(0)
detector = hands.HandDetector()
cam_surface = pygame.Surface((detector.image_size, detector.image_size))

delta_time = 0
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(jump_sound)

    ret, frame = video.read()
    if ret:
        detector.detect(frame)
        cam_surface = pygame.surfarray.make_surface(detector.annotated_image)

    if not game_over:
        if keys[pygame.K_SPACE] or detector.hand_is_open:
            player.hold_jump()

        ground.update(game_speed, delta_time)
        player.update(delta_time)
        obstacle_manager.update(game_speed, delta_time)

        if player.check_collision(obstacle_manager.obstacles):
            player.high_score = player.score
            game_over = True

        game_surface.fill("white")
        ground.draw(game_surface)
        player.draw(game_surface, text_font)
        obstacle_manager.draw(game_surface)
        game_surface.blit(cam_surface, (0, 0))
        window.blit(game_surface, (0, 0))

        if game_over: # Game freeze effect
            menu_surface = game_surface.copy()
            pygame.mixer.Sound.play(die_sound)
            obstacle_manager.reset()
            player.reset()
    else:
        if keys[pygame.K_SPACE]:
            game_over = False
        menu_surface.blit(cam_surface, (0, 0))
        window.blit(menu_surface, (0, 0))
        window.blit(game_over_message1, (200, 50))
        window.blit(game_over_message2, (80, 100))

    pygame.display.update()
    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

video.release()
pygame.quit()