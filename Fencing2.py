# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:57:43 2021

@author: Tim
"""

import pygame
from pygame.locals import *
import random
import os
import time
import neat
import visualize
import pydot
import pickle
pygame.init()
pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730

ACC = 0.5
FRIC = -0.12
FPS = 60

vec = pygame.math.Vector2
FramePerSec = pygame.time.Clock()

STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Fencing AI")

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

#fencer_images = [(pygame.image.load(os.path.join("imgs","fencer" + str(x) + ".png"))) for x in range(1,4)]
fencer_image = (pygame.image.load(os.path.join("imgs","fencer1P.png")))
high_pose_image = (pygame.image.load(os.path.join("imgs","fencer2P.png")))
low_pose_image = (pygame.image.load(os.path.join("imgs","fencer3P.png")))

base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

class Fencer(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        
        self.img_count = 0
        self.images = []
        self.images.append(fencer_image)
        self.images.append(high_pose_image)
        self.images.append(low_pose_image)
        self.image = self.images[0].convert_alpha()
        self.rect = self.image.get_rect()
        #self.mask = pygame.mask.from_surface(self.image)
        self.mask = pygame.mask.from_threshold(self.image, (145, 18, 249), (145, 18, 249))
        
        #170,730
        self.pos = vec((x, y))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        

    def move(self):
        self.acc = vec(0,0.5)
     
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC - 2
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC + 2
            
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc   
        
        
        if self.pos.x > WIN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIN_WIDTH

        self.rect.midbottom = self.pos
        

        
    def update(self):
        hits = pygame.sprite.spritecollide(Fencer1, platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0


    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
           self.vel.y = -7

    def mid_pose(self):
        self.image = self.images[0].convert_alpha()
        self.mask = pygame.mask.from_threshold(self.image, (145, 18, 249), (145, 18, 249))
        
    def high_pose(self):
        self.image = self.images[1].convert_alpha()
        self.mask = pygame.mask.from_threshold(self.image, (145, 18, 249), (145, 18, 249))
    def low_pose(self):
        self.image = self.images[2].convert_alpha()
        self.mask = pygame.mask.from_threshold(self.image, (145, 18, 249), (145, 18, 249))
        
WIDTH = base_img.get_width()          
class Floor(pygame.sprite.Sprite):
    
    
    def __init__(self, x, y):
        super().__init__() 
    
        self.x = x
        self.y = y
        self.images = []
        self.images.append(base_img)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = (WIDTH/2, y))


class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((50, 40)).convert_alpha()
        self.image.fill((128,255,40))
        self.rect = self.image.get_rect(center = (420, 460))
        self.mask = pygame.mask.from_surface(self.image)
        #self.mask = pygame.mask.from_threshold(self.image, (128,255,40), (128,255,40))
        
        
    def update(self):
        #hits = pygame.sprite.collide_mask(Box1, Fencer1)
        offset = (int(Fencer1.pos.x), int(Fencer1.pos.y))
        hits = Box1.mask.overlap(Fencer1.mask, (offset))
        print(offset, hits)
        
        if hits:
            self.image.fill((255,0,0))
            print("Hit")
        else:
            self.image.fill((128,255,40))
            

"""
class Sabre(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 

        self.pos = vec((x, y))
        self.image = pygame.Surface((150, 5))
        self.image.fill((128,255,40))
        self.rect = self.image.get_rect(center = (340, 465))
"""
        
#170,730
Fencer1 = Fencer(170,700)
Floor1 = Floor(-50,730)
Box1 = Box()
#Sabre1 = Sabre(340, 465)

all_sprites = pygame.sprite.Group()
#all_sprites.add(Sabre1)
all_sprites.add(Fencer1)

boxes = pygame.sprite.Group()
boxes.add(Box1)

platforms = pygame.sprite.Group()
platforms.add(Floor1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_UP:
                Fencer1.jump()
            if event.key == ord('z'):
                Fencer1.high_pose()
            if event.key == ord('x'):
                Fencer1.mid_pose()
            if event.key == ord('c'):
                Fencer1.low_pose()
    #Fencer(170,620).move()
    WIN.blit(bg_img, (0,0))
    #WIN.blit(base_img, (0,FLOOR))
    
    for entity in boxes:
        WIN.blit(entity.image, entity.rect)
    
    for entity in platforms:
        WIN.blit(entity.image, entity.rect)
        
    for entity in all_sprites:
        WIN.blit(entity.image, entity.rect)
        

    pygame.display.update()
    FramePerSec.tick(FPS)
    Fencer1.move()
    Fencer1.update()
    Box1.update()