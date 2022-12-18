import pygame
import sys
from src.util.settings import *
from src.util.map import mini_map
from random import randrange


class Drawing:
    def __init__(self, screen, sc_map, player, weapon, clock):
        self.root = 'res/pictures/'
        self.screen = screen
        self.sc_map = sc_map
        self.player = player
        self.weapon = weapon
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('res/font/font.ttf', 144)
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
            pygame.draw.rect(self.sc_map, DARKBROWN,
                             (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.sc_map, MAP_POS)

    def player_weapon(self, shots):
        if self.player.shot:
            if not self.weapon.shot_length_count:
                self.weapon.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon.weapon_pos)
            self.weapon.shot_animation_count += 1
            if self.weapon.shot_animation_count == self.weapon.shot_animation_speed:
                self.weapon.weapon_shot_animation.rotate(-1)
                self.weapon.shot_animation_count = 0
                self.weapon.shot_length_count += 1
                self.weapon.shot_animation_trigger = False
            if self.weapon.shot_length_count == self.weapon.shot_length:
                self.player.shot = False
                self.weapon.shot_length_count = 0
                self.weapon.sfx_length_count = 0
                self.weapon.shot_animation_trigger = True
        else:
            self.screen.blit(self.weapon.weapon_base_sprite, self.weapon.weapon_pos)

    def bullet_sfx(self):
        if self.weapon.sfx_length_count < self.weapon.sfx_length:
            sfx = pygame.transform.scale(self.weapon.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.weapon.sfx_length_count += 1
            self.weapon.sfx.rotate(-1)

    def win(self):
        render = self.font_win.render('YOU WIN!', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = HALF_WIDTH, HALF_HEIGHT
        pygame.draw.rect(self.screen, BLACK, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)


class DrawingMenu:
    def __init__(self, screen, clock):
        button_font = pygame.font.Font('res/font/font.ttf', 72)
        self.x = 0
        self.sc = screen
        self.menu_picture = pygame.image.load('res/pictures/hello_menu_pict.jpg').convert()
        self.label_font = pygame.font.Font('res/font/font1.otf', 400)
        self.start = button_font.render('START', True, pygame.Color('lightgray'))
        self.button_start = pygame.Rect(0, 0, 400, 150)
        self.button_start.center = HALF_WIDTH, HALF_HEIGHT
        self.game_exit = button_font.render('EXIT', True, pygame.Color('lightgray'))
        self.button_exit = pygame.Rect(0, 0, 400, 150)
        self.button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
        self.menu_trigger = True
        self.clock = clock

    def button_draw(self,
                    name: str,
                    border_radius: int,
                    delta_x: int,
                    delta_y: int,
                    width: int = 0) -> None:
        if name == 'start':
            pygame.draw.rect(self.sc, BLACK, self.button_start, border_radius, width)
            self.sc.blit(self.start, (
                self.button_start.centerx - delta_x, self.button_start.centery - delta_y))
        elif name == 'exit':
            pygame.draw.rect(self.sc, BLACK, self.button_exit, border_radius, width)
            self.sc.blit(self.game_exit, (
                self.button_exit.centerx - delta_x, self.button_exit.centery - delta_y))

    def menu_loop(self):
        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.sc.blit(self.menu_picture, (0, 0), (self.x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            self.x += 1

            self.button_draw('start', 25, 130, 70, 10)
            self.button_draw('exit', 25, 85, 70, 10)

            color = randrange(40)
            label = self.label_font.render('DOOMPy', True, (color, color, color))
            self.sc.blit(label, (15, -30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if self.button_start.collidepoint(mouse_pos):
                self.button_draw('start', 25, 130, 70)
                if mouse_click[0]:
                    self.menu_trigger = False
            elif self.button_exit.collidepoint(mouse_pos):
                self.button_draw('exit', 25, 85, 70)
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)
