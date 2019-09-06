import sys
import math
import time
import random
import pygame
from pygame.locals import *
from scene import Scene
from obstacles import Plant, Ptera
from dinosaur import Dinosaur

BACKGROUND = (250, 250, 250)
WIDTH = 800
HEIGHT = 400


def gameover_scene(screen, score, font):
    screen.fill(BACKGROUND)
    # head_img = pygame.image.load('./images/others/bao.png').convert_alpha()
    # head_rect = head_img.get_rect()
    # head_rect.left, head_rect.top = WIDTH // 2.5, int(HEIGHT / 6)
    # screen.blit(head_img, head_rect)
    gameover_img = pygame.image.load('./images/others/gameover.png').convert_alpha()
    gameover_rect = gameover_img.get_rect()
    gameover_rect.left, gameover_rect.top = WIDTH // 3, int(HEIGHT / 2)
    screen.blit(gameover_img, gameover_rect)
    restart_img = pygame.image.load('./images/others/restart.png').convert_alpha()
    restart_rect = restart_img.get_rect()
    restart_rect.left, restart_rect.top = int(WIDTH / 2.25), int(HEIGHT / 1.3)
    screen.blit(restart_img, restart_rect)
    pygame.display.update()

    score_text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    screen.blit(score_text, [10, 10])
    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < restart_rect.right and mouse_pos[0] > restart_rect.left and \
                        mouse_pos[1] < restart_rect.bottom and mouse_pos[1] > restart_rect.top:
                    return True


def sigmoid(score):
    probability = 1 / (1 + math.exp(-score))
    return min(probability, 0.6)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Dinosaur!")
    clock = pygame.time.Clock()
    score = 0

    # font and effects
    font = pygame.font.Font('./font/simkai.ttf', 20)
    jump_sound = pygame.mixer.Sound("./music/jump.wav")
    jump_sound.set_volume(6)
    die_sound = pygame.mixer.Sound("./music/ao.wav")
    die_sound.set_volume(6)
    pygame.mixer.init()
    pygame.mixer.music.load("./music/FiluAndDina_-_Funny_Game_Background.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    # instances
    dinosaur = Dinosaur(WIDTH, HEIGHT)
    scene = Scene(WIDTH, HEIGHT)
    plants = pygame.sprite.Group()
    pteras = pygame.sprite.Group()

    # create events
    GenPlantEvent = pygame.constants.USEREVENT + 0
    pygame.time.set_timer(GenPlantEvent, 1500)
    GenPteraEvent = pygame.constants.USEREVENT + 1
    pygame.time.set_timer(GenPteraEvent, 5000)

    # check if still running
    running = True

    #check if obstacles can be created
    flag_plant = False
    flag_ptera = False

    t0 = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
                pygame.quit()
            if event.type == GenPlantEvent:
                flag_plant = True
            if event.type == GenPteraEvent:
                if score > 20:
                    flag_ptera = True
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            dinosaur.is_jumping = True
            jump_sound.play()
        screen.fill(BACKGROUND)
        time_passed = time.time() - t0
        t0 = time.time()

        # scene
        scene.move()
        scene.draw(screen)

        #  dinosaur
        dinosaur.is_running = True
        if dinosaur.is_jumping:
            dinosaur.be_afraid()
            dinosaur.jump(time_passed)
        dinosaur.draw(screen)

        # plants
        if random.random() < sigmoid(score) and flag_plant:
            plant = Plant(WIDTH, HEIGHT)
            plants.add(plant)
            flag_plant = False
        for plant in plants:
            plant.move()
            if dinosaur.rect.left > plant.rect.right and not plant.added_score:
                score += 1
                plant.added_score = True
            if plant.rect.right < 0:
                plants.remove(plant)
                continue
            plant.draw(screen)

        # pteras
        if random.random() < sigmoid(score) and flag_ptera:
            if len(pteras) > 1:
                continue
            ptera = Ptera(WIDTH, HEIGHT)
            pteras.add(ptera)
            flag_ptera = False
        for ptera in pteras:
            ptera.move()
            if dinosaur.rect.left > ptera.rect.right and not ptera.added_score:
                score += 5
                ptera.added_score = True
            if ptera.rect.right < 0:
                pteras.remove(ptera)
                continue
            ptera.draw(screen)

        # collision detection
        if pygame.sprite.spritecollide(dinosaur, plants, False) \
            or pygame.sprite.spritecollide(dinosaur, pteras, False):
            die_sound.play()
            running = False

        # show score
        score_text = font.render('Score: ' + str(score), 1, (0, 0, 0))
        screen.blit(score_text, [10, 10])
        pygame.display.flip()
        clock.tick(60)

    res = gameover_scene(screen, score, font)

    return res

if __name__ == '__main__':
    res = True
    while res:
        res = main()
