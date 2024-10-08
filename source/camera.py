import pygame
from pygame.math import Vector2 as vec
from .config import Config
from .debug import draw_hitbox

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = vec()
        self.zoom_lvl = 2
    
    def center_on_target(self, target):
        self.offset.x = target.rect.centerx - (Config.WINDOW_SIZE[0]//2) / self.zoom_lvl
        self.offset.y = target.rect.centery - (Config.WINDOW_SIZE[1]//2) / self.zoom_lvl
        
    def custom_draw(self, player, debug):
        
        self.center_on_target(player)

        sprites = [sprite for sprite in self]
        for sprite in sprites:
            offset_pos = (sprite.rect.topleft - self.offset) * self.zoom_lvl

            scaled_image = pygame.transform.scale(sprite.image, 
                                        (int(sprite.rect.width * self.zoom_lvl), 
                                        int(sprite.rect.height * self.zoom_lvl)))
            
            self.screen.blit(scaled_image, offset_pos)
            ### DEBUG
            if debug:
                if hasattr(sprite, 'hitbox'):
                    if sprite.hitbox:
                        hitbox_offset_pos = (sprite.hitbox.topleft - self.offset) * self.zoom_lvl

                        scaled_hitbox = pygame.Rect(hitbox_offset_pos,
                            (int(sprite.hitbox.width * self.zoom_lvl), 
                            int(sprite.hitbox.height * self.zoom_lvl))
                        )
                        draw_hitbox(self.screen, scaled_hitbox.topleft, scaled_hitbox.size)
            ### DEBUG END