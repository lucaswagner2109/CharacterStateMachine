import pygame

from .config import Config

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.image = pygame.Surface((32, 32))
        self.image.fill((Config.WHITE))
        self.rect = self.image.get_frect(topleft = pos)