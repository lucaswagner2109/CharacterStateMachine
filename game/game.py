from .config import Config
from .player import Player
from .sprites import Tile

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
        for row_idx, row in enumerate(Config.LAYOUT):
            for col_idx, col in enumerate(row):
                if col == 1:
                    y = row_idx * Config.TILE_SIZE
                    x = col_idx * Config.TILE_SIZE
                
                    Tile((x, y), [self.sprites, self.collision_sprites])
        
        for row_idx, row in enumerate(Config.LAYOUT):
            for col_idx, col in enumerate(row):
                if col == 2:
                    y = row_idx * Config.TILE_SIZE
                    x = col_idx * Config.TILE_SIZE
                
                    self.player = Player((x, y), self.sprites, self.collision_sprites)

    def run(self, debug):
        if debug:
            print("Debug mode.")
        
        while True:
            dt = self.clock.tick(Config.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
  
            self.screen.fill(Config.BLACK)
                    
            self.sprites.update(dt)
            self.sprites.draw(self.screen)
            
            pygame.display.update()