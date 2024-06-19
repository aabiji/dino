import pygame
from game import Ground, Player, Obstacles

# TODO: mediapipe integration
# TODO: install model automatically if we haven't already
# TODO: flatten assets folder

win_width = 600
win_height = 500
pygame.init()
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Dino")
game_surface = pygame.Surface((win_width, win_height))
menu_surface = pygame.Surface((win_width, win_height))

font_path = "assets/PressStart2P-Regular.ttf"
text_font = pygame.font.Font(font_path, 15)
msg_font = pygame.font.Font(font_path, 20)
game_over_message1 = msg_font.render("Game over", False, (0, 0, 0))
game_over_message2 = msg_font.render("Press Space to restart", False, (0, 0, 0))

clock = pygame.time.Clock()
fps = 60
game_speed = 300

ground = Ground(win_height)
player = Player(win_height)
obstacle_manager = Obstacles(win_width, win_height)
game_over = False

delta_time = 0
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        if keys[pygame.K_SPACE]:
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
        window.blit(game_surface, (0, 0))

        if game_over: # Game freeze effect
            menu_surface = game_surface.copy()
            obstacle_manager.reset()
            player.reset()
    else:
        if keys[pygame.K_SPACE]:
            game_over = False
        window.blit(menu_surface, (0, 0))
        window.blit(game_over_message1, (200, 50))
        window.blit(game_over_message2, (80, 100))

    pygame.display.update()
    time_spent = clock.tick(fps)
    delta_time = time_spent / 1000

pygame.quit()