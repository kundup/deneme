import pygame
from pygame import locals
pygame.init()

clock = pygame.time.Clock()
# Font
font_score = pygame.font.Font("Pixeltype.ttf", 40)
font_surf = font_score.render("My time: ", False, (0, 0, 0))
font_rect = font_surf.get_rect(midbottom=(400, 50))

# display surface
screen = pygame.display.set_mode((800, 400))

# sky surface, ground surface
sky_surface = pygame.image.load("Sky.png").convert()
ground_surface = pygame.image.load("ground.png").convert()

# Player config
player_surface = pygame.image.load("player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(90, 300))

# snail config
snail_surface = pygame.image.load("snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(700, 300))
player_gravity = 0
def snail_move():
    snail_rect.x -= 6
    if snail_rect.x < -50: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20



    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300: player_rect.bottom = 300
    screen.blit(player_surface, player_rect)
    # snail movement
    snail_move()
    screen.blit(font_surf, font_rect)

    pygame.display.update()
    clock.tick(60)


pygame.quit()
