import pygame as pg

from utils import *

class Body:
    
    def __init__(self, init_pos: v2):
        self.sprite = pg.image.load('assets/body.png').convert_alpha()
        self.rect = self.sprite.get_rect()
        self.rect.topleft = init_pos
        self.previous_pos = v2(0, 0)
        