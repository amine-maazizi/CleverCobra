import pygame as pg
from random import randint

from utils import *

class Apple:
    
    def __init__(self, pos_to_avoid: v2):
        self.sprite = pg.image.load('assets/apple.png')
        self.rect = self.sprite.get_rect()
        self.pos_to_avoid = pos_to_avoid
        self.respawn()
    
    def render(self, display: pg.Surface):
        display.blit(self.sprite, self.rect)
    
    def respawn(self):
        x, y = randint(0, HEIGHT / TILE_SIZE - 1) * TILE_SIZE, randint(0, WIDTH / TILE_SIZE - 1) * TILE_SIZE 
        while (v2(x, y) == self.pos_to_avoid):
            x, y = randint(0, HEIGHT / TILE_SIZE - 1) * TILE_SIZE, randint(0, WIDTH / TILE_SIZE - 1) * TILE_SIZE 
        self.rect.top = x
        self.rect.left = y