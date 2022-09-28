import pygame
from util.settings import *
from map import mini_map

class Drawing():
    def __init__(self, screen, sc_map):
        self.root = 'res/pictures/'
        self.screen = screen
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {
            1: pygame.image.load(f'{self.root}wall1.png').convert(),
            2: pygame.image.load(f'{self.root}wall2.png').convert(),
            3: pygame.image.load(f'{self.root}wall3.png').convert(),
            4: pygame.image.load(f'{self.root}wall4.png').convert(),
            5: pygame.image.load(f'{self.root}wall5.png').convert(),
            6: pygame.image.load(f'{self.root}wall6.png').convert(),
            'S': pygame.image.load(f'{self.root}sky1.png').convert()
            }


    def background(self, angle):
        sky_offset = -15 * math.degrees(angle) % WIDTH
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(
            self.screen, DARKGREY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT)
            )

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)


    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, DARKORAGE)
        self.screen.blit(render, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), 
                        (map_x + 12 * math.cos(player.angle),
                        map_y + 12 * math.sin(player.angle)), 5
                        )
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, DARKBROWN, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.sc_map, MAP_POS)