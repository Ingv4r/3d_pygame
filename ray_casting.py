import pygame
from settings import *
from map import world_map

#def ray_casting(screen, player_pos, player_angle):
#    cur_angle = player_angle - HALF_FOV
#    xo, yo = player_pos
#    for ray in range(NUM_RAYS):
#        sin_a = math.sin(cur_angle)
#        cos_a = math.cos(cur_angle)
#        for depth in range(MAX_DEPTH):
#            x = xo + depth * cos_a
#            y = yo + depth * sin_a
#            #pygame.draw.line(screen, DARKGREY, player_pos, (x, y), 2)
#            if (x // TILE * TILE, y // TILE * TILE) in world_map:
#                depth *= math.cos(player_angle - cur_angle)
#                proj_height = PROJ_COEF / depth
#                c = 255 / (1 + depth * depth * 0.00002)
#                color = (c, c // 2, c // 3)
#                pygame.draw.rect(screen, color,
#                    (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height
#                    ))
#                break
#        cur_angle += DELTA_ANGLE
def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE

def ray_casting(screen, player_pos, player_angle, texture):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        #verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            if mapping(x + dx, yv) in world_map:
                break
            x += dx * TILE

        #horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            if mapping(xh, y + dy) in world_map:
                break
            y += dy * TILE

        #projection
        depth, offset = (depth_v, yv) if depth_v < depth_h else (depth_h, xh)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(PROJ_COEF / depth), 2 * HEIGHT)
        
        cur_angle += DELTA_ANGLE
                
        