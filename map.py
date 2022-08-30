from settings import *

text_map = [
    'WWWWWWWWWWWW',
    'w..........w',
    'w...WW.....w',
    'w...W......w',
    'w...W......w',
    'w..........w',
    'w..........w',
    'WWWWWWWWWWWW'
]

world_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * TITLE, j * TITLE))