import pygame
from pygame.math import Vector2 as vec
from .config import Config
from .debug import draw_hitbox

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = vec()
    
    def center_on_target(self, target):
        self.offset.x = target.rect.centerx - Config.WINDOW_SIZE[0]//2
        self.offset.y = target.rect.centery - Config.WINDOW_SIZE[1]//2
        
    def custom_draw(self, player, debug):
        
        self.center_on_target(player)

        sprites = [sprite for sprite in self]
        for sprite in sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)
            if debug:
                if hasattr(sprite, 'hitbox'):
                    if sprite.hitbox:
                        rect_offset_pos = sprite.hitbox.topleft - self.offset
                        draw_hitbox(sprite, self.screen, rect_offset_pos)