from .config import Config
from .player import Player

import pygame, sys

class Game():
    
    def __init__(self, debug):
        self.debug = debug
        pygame.init()
        pygame.display.set_caption(Config.GAME_TITLE)
        self.screen = pygame.display.set_mode(Config.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        
        self.sprites = pygame.sprite.Group()
        self.player = Player((Config.WINDOW_SIZE[0]//2, Config.WINDOW_SIZE[1]//2), self.sprites)

    def run(self):
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