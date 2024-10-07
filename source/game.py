from .config import Config
from .player import Player
from .sprites import Tile
from .support import import_sprites_folder
from .debug import draw_info

import pygame, sys

class Game():
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Config.GAME_TITLE)
        self.screen = pygame.display.set_mode(Config.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        
        self.sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup()

    def setup(self):
        # setup tiles
        for row_idx, row in enumerate(Config.LAYOUT):
            for col_idx, col in enumerate(row):
                if col == 1:
                    y = row_idx * Config.TILE_SIZE
                    x = col_idx * Config.TILE_SIZE
                
                    Tile((x, y), [self.sprites, self.collision_sprites])
        
        # setup player
        for row_idx, row in enumerate(Config.LAYOUT):
            for col_idx, col in enumerate(row):
                if col == 2:
                    y = row_idx * Config.TILE_SIZE
                    x = col_idx * Config.TILE_SIZE
                
                    self.player = Player(
                        pos=(x, y), 
                        groups=self.sprites, 
                        frames=import_sprites_folder("assets/player"),
                        collision_sprites=self.collision_sprites)

    def run(self, debug):
        while True:
            dt = self.clock.tick(Config.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
  
            self.screen.fill(Config.BLACK)
                    
            self.sprites.update(dt)
            self.sprites.draw(self.screen)
            
            if debug:
                info = f"Facing: {self.player.facing}, State: {self.player.state}"
                draw_info(info = info, screen = self.screen)
            
            pygame.display.update()