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
fencer_image = (pygame.image.load(os.path.join("imgs","fencer1.png")))

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
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
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
           self.vel.y = -15
            
WIDTH = base_img.get_width()          
class Floor(pygame.sprite.Sprite):
    
    
    def __init__(self, x, y):
        super().__init__() 
    
        self.x = x
        self.y = y
        self.images = []
        self.images.append(base_img)
        self.img = self.images[0]
        self.rect = self.img.get_rect(center = (WIDTH/2, y))


class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((30, 30))
        self.image.fill((128,255,40))
        self.rect = self.image.get_rect(center = (420, 350))

        
    def update(self):
        hits = pygame.sprite.collide_mask(Box1, Fencer1)
        if hits:
            self.image.fill((255,0,0))
            print("Hit")
        else:
            self.image.fill((128,255,40))
            
#170,730
Fencer1 = Fencer(170,700)
Floor1 = Floor(-50,730)
Box1 = Box()

all_sprites = pygame.sprite.Group()
#all_sprites.add(Box1)
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
    
    #Fencer(170,620).move()
    WIN.blit(bg_img, (0,0))
    #WIN.blit(base_img, (0,FLOOR))
    
    for entity in boxes:
        WIN.blit(entity.image, entity.rect)
    
    for entity in platforms:
        WIN.blit(entity.img, entity.rect)
        
    for entity in all_sprites:
        WIN.blit(entity.image, entity.rect)
        

    pygame.display.update()
    FramePerSec.tick(FPS)
    Fencer1.move()
    Fencer1.update()
    Box1.update()