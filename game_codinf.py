import pygame

pygame.init()

clock = pygame.time.Clock()
# Font
font_score = pygame.font.Font("Pixeltype.ttf", 40)
font_surf = font_score.render("My time: ", False, (0, 0, 0))
font_rect = font_surf.get_rect(midbottom=(400, 50))
total_score = 0

# font config for restart window
restart_window = font_score.render("Press Spc to Run", False, (255, 255, 255))
restart_window = pygame.transform.rotozoom(restart_window, 0, 1.6)
restart_window_rect = restart_window.get_rect(center=(400, 50))

# display surface
screen = pygame.display.set_mode((800, 400))

# sky surface, ground surface
sky_surface = pygame.image.load("Sky.png").convert()
ground_surface = pygame.image.load("ground.png").convert()

# Player config
player_surface = pygame.image.load("player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(90, 300))

# player config for restart page
player_stand = pygame.transform.rotozoom(player_surface, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# snail config
snail_surface = pygame.image.load("snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(700, 300))
player_gravity = 0

# fly config
fly_surface = pygame.image.load("fly1.png").convert_alpha()
fly_rect = snail_surface.get_rect(midbottom=(900, 210))

# game status
game_active = 1

# game score added
game_score = 0


def display_score():
    current_time = (pygame.time.get_ticks() - game_score) // 1000
    score_surf = font_score.render(f"My Score: {current_time}", False, (0, 0, 0))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def snail_move():
    snail_rect.x -= 11
    if snail_rect.x < -50: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)


def fly_move():
    fly_rect.x -= 9
    if fly_rect.x <= -50: fly_rect.left = 800
    screen.blit(fly_surface, fly_rect)


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = 1
                snail_rect.left, fly_rect.left = 790, 850
                game_score = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # player y direction movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # font surface
        total_score = display_score()

        # snail movement
        snail_move()

        # fly movement
        fly_move()

        # collison
        if snail_rect.colliderect(player_rect) or fly_rect.colliderect(player_rect):
            game_active = 0

    else:
        screen.fill((90, 120, 160))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(restart_window, restart_window_rect)
        score_message = font_score.render(f"Your Score: {total_score}", False, (255, 255, 255))
        score_message_rect = score_message.get_rect(center=(400, 315))
        screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
