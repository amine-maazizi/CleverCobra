from typing import Tuple
from enum import Enum
import pygame as pg

WIDTH: int = 512
HEIGHT: int = 512
GUI_PADDING: int = 160

FPS: int = 60

BG_COLOR: Tuple[int, int, int] = (0, 0, 0)
FG_COLOR: Tuple[int, int, int] = (255, 255, 255)

TILE_SIZE: int = 16
WAIT_TIME: int = 1

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
ALPHA = 0.001

v2 = pg.math.Vector2

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    
class CollisionType(Enum):
    FOOD = 1
    BODY = 2
    NOTHING = 3