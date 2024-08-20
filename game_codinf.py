import pygame
from random import randint, random
import json
from spritesheet import ParticleStar
from time import time

pygame.init()

# import ParticleStar and creating new instance
confetti_effect = ParticleStar("star.png")

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

# display surface and game name
screen = pygame.display.set_mode((800, 400))
game_name = pygame.display.set_caption("Creator")

# sky surface, ground surface
sky_surface = pygame.image.load("Sky.png").convert()
ground_surface = pygame.image.load("ground.png").convert()

# Player config
player_anime_1 = pygame.image.load("player_walk_1.png").convert_alpha()
player_anime_2 = pygame.image.load("player_walk_2.png").convert_alpha()
player_surface = [player_anime_1, player_anime_2]
player_index = 0
player_rect = player_surface[player_index].get_rect(midbottom=(90, 300))

# player config for restart page
player_stand = pygame.transform.rotozoom(player_anime_1, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 210))

# snail config
snail_anime1 = pygame.image.load("spider_walk1.png").convert_alpha()
snail_anime2 = pygame.image.load("spider_walk2.png").convert_alpha()
# snail_rect = snail_surface.get_rect(midbottom=(900, 300))
snail_animation = [snail_anime1, snail_anime2]
snail_index = 0
snail_surface = snail_animation[snail_index]

player_gravity = 0

# fly config
fly_anime1 = pygame.image.load("Fly1.png").convert_alpha()
fly_anime2 = pygame.image.load("Fly2.png").convert_alpha()
fly_animation = [fly_anime1, fly_anime2]
fly_index = 0
fly_surface = fly_animation[fly_index]
# fly_rect = snail_surface.get_rect(midbottom=(900, 210))

# enemy list
enemy_rect_list = []

# game status
game_active = False

# game score added
game_score = 0
start_time = 0
high_score_broken = True

# data file for high score log
data = {"highest": 0}
with open("data.txt") as high_file:
    data = json.load(high_file)

# game music
background_music = pygame.mixer.Sound("music.wav")
background_music.play(loops=-1)


def display_score():
    current_time = (pygame.time.get_ticks() - game_score) // 1000
    score_surf = font_score.render(f"My Score: {current_time}", False, (0, 0, 0))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def enemy_movement(enemy_list):
    if enemy_list:
        for enemy in enemy_list:
            enemy.x -= 6.5
            if enemy.bottom == 300:
                screen.blit(snail_surface, enemy)

            else:
                screen.blit(fly_surface, enemy)

        enemy_list = [enemy for enemy in enemy_list if enemy.x >= -100]
        return enemy_list
    else:
        return []


def collision(player_rect, enemy):
    if enemy:
        for i in enemy:
            if player_rect.colliderect(i): return False
    return True


def higher_score():
    global data, start_time, high_score_broken
    if total_score > data["highest"]:
        data["highest"] = total_score
        if not confetti_effect.effect_active and high_score_broken:  # Efekt zaten aktif değilse
            confetti_effect.trigger_confetti_effect()
            high_score_broken = False

    # def snail_move():

#     snail_rect.x -= randint(9,11)
#     if snail_rect.x <=-50: snail_rect.left = randint(790, 900)
#     screen.blit(snail_surface, snail_rect)


# def fly_move():
#   fly_rect.x -= randint(8, 10)
#   if fly_rect.x <= -50: fly_rect.left = randint(800, 850)
#   screen.blit(fly_surface, fly_rect)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 900)

fly_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_timer, 200)

snail_timer = pygame.USEREVENT + 3
pygame.time.set_timer(snail_timer, 300)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data.txt", "w") as high_score_file:
                json.dump(data, high_score_file)
            running = False

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == enemy_timer:
                if randint(0, 2):
                    enemy_rect_list.append(snail_surface.get_rect(midbottom=(800, 300)))
                else:
                    enemy_rect_list.append(fly_surface.get_rect(midbottom=(800, 210)))

            if event.type == fly_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_animation[fly_index]

            if event.type == snail_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_animation[snail_index]



        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left, fly_rect.left = randint(795, 1050), randint(800, 950)
                game_score = pygame.time.get_ticks()
                high_score_broken = True

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # player y direction movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300

        # player animation
        player_index += 0.15
        if player_index >= 2: player_index = 0
        screen.blit(player_surface[int(player_index)], player_rect)

        enemy_rect_list = enemy_movement(enemy_rect_list)

        # font surface
        total_score = display_score()
        higher_score()

        if confetti_effect.effect_active:
            confetti_effect.add_confetti(randint(0, 800), randint(0, 400))
            confetti_effect.move_confetti()
            confetti_effect.draw_confetti(screen)
            confetti_effect.update()

            # snail movement
        # snail_move()

        # fly movement
        # fly_move()

        # collison
        # if snail_rect.colliderect(player_rect) or fly_rect.colliderect(player_rect):
        #     game_active = False
        game_active = collision(player_rect, enemy_rect_list)
    else:
        screen.fill((90, 120, 160))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(restart_window, restart_window_rect)

        high = font_score.render(f'High score: {data["highest"]}', False, (255, 255, 255))
        high_rect = high.get_rect(center=(400, 95))
        # Game Entry restoration
        if total_score != 0:
            score_message = font_score.render(f"Your Score: {total_score}", False, (255, 255, 255))
        else:
            score_message = font_score.render(f" Wellcome to the Game ", False, (255, 255, 255))

        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(score_message, score_message_rect)
        screen.blit(high, high_rect)

        enemy_rect_list.clear()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# updates:
# new enemy adding (done)
# higher score added(done)
# entry screen (done)
# character profile changes (done)
# player run animation (done)
# adding effects when breaking high score (done)
# binary format and downloadable (done by pyinstaller name --onefile --windowed)
# player jump animation
# after some points, creating weather conditions accordingly difficulty level
# keep logs (asking user name and assign user name to the high point)
# more player character selection option at the beginning screen
# fire ball adding

