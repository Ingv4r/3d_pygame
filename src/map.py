from util.settings import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import float64

_ = False

matrix_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,4,6,_,_,_,_,_,_,_,_,_,_,6,4,_,_,_,_,1],
    [1,_,_,_,_,_,_,5,_,_,_,_,_,_,_,_,5,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,3,_,_,_,_,_,_,_,_,_,_,_,_,_,_,3,_,_,_,1],
    [1,_,_,_,3,_,_,_,_,_,_,_,_,_,_,_,_,_,_,3,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,2,2,_,_,_,_,2,2,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,2,2,2,2,2,2,_,_,_,_,_,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(float64, 2), value_type=float64)
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map[(i * TILE, j * TILE)] = 5
            elif char == 6:
                world_map[(i * TILE, j * TILE)] = 6
