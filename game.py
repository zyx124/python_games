import pygame
import random
from sys import exit
pygame.init()

screen=pygame.display.set_mode((800,450),0,32)
# set size of the background
pygame.display.set_caption('Hello world!')
background=pygame.image.load('cup.jpg').convert()

class Plane:
    def restart(self):
        self.x = 200
        self.y = 600
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()
    def move(self):
        x,y = pygame.mouse.get_pos()
        x-= self.image.get_width()/2
        y-= self.image.get_width()/2
        self.x=x
        self.y=y


class Bullet:
    def __init__(self):
        self.x=0
        self.y=-1
        self.image=pygame.image.load('bullet.jpg').convert_alpha()
        self.active=False
    def move(self):
        if self.active:
            self.y-=3
        if self.y<0:
            self.active=False
    def restart(self):
        mouseX,mouseY=pygame.mouse.get_pos()
        self.x=mouseX-self.image.get_width()/2
        self.y=mouseY-self.image.get_height()/2
        self.active=True

class Enemy:
    def __init__(self):
        self.x=200
        self.y=-50
        self.image=pygame.image.load('enemy.png').convert_alpha()

    def move(self):
        if self.y < 450:
            self.y += 0.3
        else:
            self.restart()
    def restart(self):
        self.x=random.randint(0,800)
        self.y=random.randint(-200,-50)
        self.speed = random.random()+0.3


def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    return False

def checkCrash(enemy,plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height()> enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False

plane=Plane()

bullets=[]

# introduce 5 bullets
for i in range(5):
    bullets.append(Bullet())
# total number of bullets
count_b=len(bullets)
# the index of the next reactive bullet
index_b=0
# interval butween 2 bullets
interval_b=0

enemies=[]
for i in range(10):
    enemies.append(Enemy())

gameover = False
score = 0

font=pygame.font.Font(None, 60)

#main loop
while True:
    
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background,(0,0))

    interval_b -= 1
    if interval_b < 0:
        bullets[index_b].restart()
        interval_b = 100
        index_b = (index_b+1) % count_b

    if not gameover:
        for e in enemies:
            if checkCrash(e, plane):
                gameover = True
        e.move()
        screen.blit(e.image,(e.x,e.y))

    if gameover == True:
        over = font.render('Crash! Game Over!',1, (0,0,0))
        screen.blit(over, (100, 200))

    for b in bullets:
        if b.active:
            for e in enemies:
                if checkHit(e, b):
                    score += 100
            b.move()
            screen.blit(b.image, (b.x, b.y))
            
    text = font.render('Score: %d' % score, 1, (0,0,0))
    screen.blit(text, (400,40))
    plane.move()
    screen.blit(plane.image, (plane.x, plane.y))

    #restart the game 
    if gameover and event.type == pygame.MOUSEBUTTONUP:
        plane.restart()
        for e in enemies:
            e.restart()
        for b in bullets:
            b.active = False
        score = 0
        gameover = False
    pygame.display.update()
