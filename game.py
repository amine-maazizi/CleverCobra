import pygame as pg
from pygame.locals import *
import sys

from utils import *

from snake import Snake
from apple import Apple
from gui import GUI




class Game:
    
    def __init__(self):
        pg.init()
        pg.display.set_caption('Snake AI')
        
        self.display = pg.display.set_mode([WIDTH + GUI_PADDING, HEIGHT])
        self.clock = pg.time.Clock()
        
        self.reset()
        
    def process(self):
        self.snake.process()
        self.handle_collisions()
                
    def render(self):
        self.snake.render(self.display)
        self.apple.render(self.display)
        
        self.render_grid()
        
        self.gui.render(self.display)
        
    def play_step(self, action=None):
        self.frame_iteration += 1
        
        for ev in pg.event.get():
                if (ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE)):
                    pg.quit()
                    sys.exit()
        
                if (ev.type == KEYDOWN):
                    if (ev.key == K_RIGHT):
                        self.snake.dirname = Direction.RIGHT
                    if (ev.key == K_LEFT):
                        self.snake.dirname = Direction.LEFT
                    if (ev.key == K_UP):
                        self.snake.dirname = Direction.UP
                    if (ev.key == K_DOWN):
                        self.snake.dirname = Direction.DOWN
        
        reward = 0
        
        pg.display.set_caption("%.2f FPS" % self.clock.get_fps())
        self.display.fill(BG_COLOR)
        
        self.snake.process(action)
        collision_type = self.handle_collisions()
          
        if collision_type == CollisionType.BODY or self.frame_iteration > 100 * WAIT_TIME * len(self.snake.body):
            return -10, True, self.gui.score
        
        if collision_type == CollisionType.FOOD:
            reward = 10
        
        
        self.render()
         
        self.clock.tick(FPS)
        pg.display.flip()
        
        return reward, collision_type == CollisionType.BODY, self.gui.score
        
    def run(self):
        while True:
            for ev in pg.event.get():
                if (ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE)):
                    pg.quit()
                    sys.exit()

            pg.display.set_caption("%.2f FPS" % self.clock.get_fps())
            self.display.fill(BG_COLOR)
        
            self.process()
            self.render()

            self.clock.tick(FPS)
            pg.display.update()
    
    def render_grid(self):
        for x in range(WIDTH // TILE_SIZE + 1):
            pg.draw.line(self.display, FG_COLOR, (x * TILE_SIZE, 0), (x * TILE_SIZE, HEIGHT))
        for y in range(HEIGHT // TILE_SIZE + 1):
            pg.draw.line(self.display, FG_COLOR, (0, y * TILE_SIZE), (WIDTH, y * TILE_SIZE))
    
    def handle_collisions(self):
        # Snake-Apple Collision
        headrect = self.snake.body[0].rect
        if (headrect.colliderect(self.apple.rect)):
            self.gui.increment_score()
            self.apple.respawn()
            self.snake.add_body()
            return CollisionType.FOOD
        # Snake-Body Collision
        for b in self.snake.body[2:]:
            if (headrect.colliderect(b.rect)):
                return CollisionType.BODY
        return CollisionType.NOTHING
                
    def reset(self):
        self.gui = GUI()
        self.snake = Snake()
        self.apple = Apple(self.snake.real_position)
        self.frame_iteration = 0
