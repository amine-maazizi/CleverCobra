import pygame as pg

from utils import *

class GUI:
    
    def __init__(self):
        self.font = pg.font.SysFont('arial', 24)
        self.score = 0
        self.gen = 0
        self.record = 0

    def increment_score(self):
        self.score += 1
    
    def increment_gen(self):
        self.gen += 1

    def set_score(self, score):
        self.score = score
    
    def set_gen(self, gen):
        self.gen = gen

    def set_record(self, record):
        self.record = record

    def render(self, display):
        score_text = self.font.render(f'Score: {self.score}', True, FG_COLOR)
        gen_text = self.font.render(f'Generation: {self.gen}', True, FG_COLOR)
        rec_text = self.font.render(f'Record: {self.record}', True, FG_COLOR)
        display.blit(score_text, (GUI.center_text_position(score_text), 0))
        display.blit(gen_text, (GUI.center_text_position(gen_text), 36))
        display.blit(rec_text, (GUI.center_text_position(rec_text), 72))
        
    @staticmethod
    def center_text_position(surf: pg.Surface):
        return WIDTH + GUI_PADDING / 2 - surf.get_width() / 2