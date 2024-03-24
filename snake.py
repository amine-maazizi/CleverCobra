import pygame as pg
from pygame.locals import *
from random import randint
import numpy as np

from utils import *
from body import Body

class Snake:
    
    def __init__(self):
        init_pos = v2(randint(0, WIDTH / TILE_SIZE) * TILE_SIZE, randint(0, HEIGHT / TILE_SIZE) * TILE_SIZE)
        self.dirname = Direction.RIGHT
        self.dir = v2(1, 0)  # Initial direction to the right
        
        self.body = [Body(init_pos)]
        self.add_body()
        self.add_body()
        
        self.real_position = init_pos  # Real position for smooth movement
        self.movement_cooldown = 0  # Cooldown to manage movement speed

    def process_input(self):
        pressed = pg.key.get_pressed()
        
        if pressed[K_LEFT] and self.dir.x == 0:  # Prevent immediate 180° turn
            self.dir = v2(-1, 0)
        elif pressed[K_RIGHT] and self.dir.x == 0:
            self.dir = v2(1, 0)
        elif pressed[K_UP] and self.dir.y == 0:
            self.dir = v2(0, -1)
        elif pressed[K_DOWN] and self.dir.y == 0:
            self.dir = v2(0, 1)

    def ai_input(self, action):
        
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.dirname)
        
        if (np.array_equal(action, [1, 0, 0])):
            self.dirname = clockwise[idx]
        elif (np.array_equal(action, [0, 1, 0])):
            self.dirname = clockwise[(idx + 1) % 4]
        else:
            self.dirname = clockwise[(idx - 1) % 4]  
        
        if self.dirname == Direction.RIGHT and self.dir.x == 0:
            self.dir = v2(1, 0)
        if self.dirname == Direction.LEFT and self.dir.x == 0:
            self.dir = v2(-1, 0)
        if self.dirname == Direction.UP and self.dir.y == 0:
            self.dir = v2(0, -1)
        if self.dirname == Direction.DOWN and self.dir.y == 0:
            self.dir = v2(0, 1)

    def process(self, action=None):
        # Process input on every frame
        if action:
            self.ai_input(action)
        else:
            self.ai_input([1, 0, 0])

        # self.process_input()

        # Move snake based on a cooldown to control speed
        if self.movement_cooldown <= 0:
            self.update_body_positions()
            self.move_snake()
            # Reset cooldown (adjust number for desired speed, lower is faster)
            self.movement_cooldown = WAIT_TIME
        else:
            # Decrease cooldown
            self.movement_cooldown -= 1

    def render(self, display: pg.Surface):
        for body in self.body:
            display.blit(body.sprite, body.rect)
    
    def move_snake(self):
        # Moving the snake head based on the direction, snapping to grid
        next_position = self.real_position + self.dir * TILE_SIZE
        
        # Screen wrapping logic
        if next_position.x < 0:
            next_position.x = WIDTH - TILE_SIZE  # Wrap to the right side
        elif next_position.x >= WIDTH:
            next_position.x = 0  # Wrap to the left side
            
        if next_position.y < 0:
            next_position.y = HEIGHT - TILE_SIZE  # Wrap to the bottom
        elif next_position.y >= HEIGHT:
            next_position.y = 0  # Wrap to the top

        self.real_position = next_position
        self.body[0].rect.topleft = self.real_position

        # Apply screen wrapping for the rest of the body
        for segment in self.body[1:]:
            if segment.rect.left < 0:
                segment.rect.left = WIDTH - TILE_SIZE
            elif segment.rect.left >= WIDTH:
                segment.rect.left = 0
                
            if segment.rect.top < 0:
                segment.rect.top = HEIGHT - TILE_SIZE
            elif segment.rect.top >= HEIGHT:
                segment.rect.top = 0


    def update_body_positions(self):
        # Store the previous position to update the following segment
        for i in range(len(self.body) - 1, 0, -1):
            # Each segment takes the position of the segment in front of it
            self.body[i].rect.topleft = self.body[i-1].rect.topleft
        
    def add_body(self):
        # Ensure we have at least one segment to reference
        if self.body:
            last_segment = self.body[-1]
            # Calculate the opposite direction for the initial placement
            opposite_direction = -self.dir * TILE_SIZE
            new_position = (last_segment.rect.left + opposite_direction.x, last_segment.rect.top + opposite_direction.y)
            new_segment = Body(new_position)
            self.body.append(new_segment)

