import pygame
import sys
import random

is_pause = False
pygame.init()
screen = pygame.display.set_mode((576, 650))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19__.TTF", 40)
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
highscore = 0
canscore = True
bg_surface = pygame.image.load('3background-day.png').convert()
floor_surface = pygame.image.load("base.png").convert()
floor_x_pos = 0
bird_downflap = pygame.image.load("bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 2
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 325))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
pipe_surface = pygame.image.load("pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [350, 400, 500]
game_over_surface = pygame.image.load("message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288, 325))
flap_sound = pygame.mixer.Sound("wing.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
score_sound = pygame.mixer.Sound('point.wav')
score_sound_countdown = 100


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 550))
    screen.blit(floor_surface, (floor_x_pos + 576, 550))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visiblepipes = [pipe for pipe in pipes if pipe.right > -50]
    return visiblepipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 650:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global canscore
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            canscore = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 550:
        canscore = True
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def update_score(score, highscore):
    if score > highscore:
        highscore = score
    return highscore


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score:{int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f"High Score:{int(highscore)}", True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(250, 500))
        screen.blit(high_score_surface, high_score_rect)


def pipe_score_check():
    global score, canscore
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and canscore:
                score += 1
                score_sound.play()
                canscore = False
            if pipe.centerx < 0:
                canscore = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 325)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    screen.blit(bg_surface, (0, 0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()
        score_display("main_game")

    else:
        screen.blit(game_over_surface, game_over_rect)
        highscore = update_score(score, highscore)
        score_display('game_over')
        # level = 1
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)

    # if score == 5 and level == 1:
    #     level += 1
    #     gravity += 0.1
    # if score == 10 and level == 2:
    #     level += 1
    #     gravity += 0.1
    # if score == 15 and level == 3:
    #     level += 1
    #     gravity += 0.1
    # if score == 20 and level == 4:
    #     level += 1
    #     gravity += 0.1
