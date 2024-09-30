from .config import Config

import pygame

from pygame.math import Vector2 as vec

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # Components
        self.input = PlayerInput(self)
        self.movement = PlayerMovement(self, collision_sprites)
        
        # Sprite variables                                                 
        self.image = pygame.Surface((32, 32))
        self.image.fill((Config.RED))
        self.rect = self.image.get_frect(topleft = pos)
        self.prev_rect = self.rect.copy()
        
        # Movement variables
        self.direction_vec = vec()
        self.input_disabled = False
        self.jump = False
               
    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.input.update()
        self.movement.move(dt)
        
class PlayerInput:
    
    def __init__(self, player):
        self.player = player
        
    def input(self):
        input_vec = vec()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            input_vec.x += -1
        elif keys[pygame.K_d]:
            input_vec.x += 1
        
        if keys[pygame.K_SPACE]:
            self.player.jump = True
            
        self.player.direction_vec.x = input_vec.normalize().x if input_vec else 0
            
    def update(self):
        if not self.player.input_disabled:
            self.input()
            
class PlayerMovement:
    
    def __init__(self, player, collision_sprites):
        self.player = player
        self.collision_sprites = collision_sprites
        
    def move(self, dt):
        self.player.rect.x += self.player.direction_vec.x * Config.PLAYER_RUN_SPEED * dt
        self.check_collision("h")
        
        self.player.direction_vec.y += Config.GRAVITY / 2 * dt
        self.player.rect.y += self.player.direction_vec.y * dt
        self.player.direction_vec.y += Config.GRAVITY / 2 * dt
        
        self.check_collision("v")
        
        if self.player.jump:
            self.player.direction_vec.y = -Config.PLAYER_JUMP_STRENGTH
            self.player.jump = False
        
    def check_collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.player.rect):
                if axis == "h":
                    if self.player.rect.left <= sprite.rect.right and self.player.prev_rect.left >= sprite.prev_rect.right:
                        self.player.rect.left = sprite.rect.right
                    if self.player.rect.right >= sprite.rect.left and self.player.prev_rect.right <= sprite.prev_rect.left:
                        self.player.rect.right = sprite.rect.left
                else:
                    if self.player.rect.top <= sprite.rect.bottom and self.player.prev_rect.top >= sprite.prev_rect.bottom:
                        self.player.rect.top = sprite.rect.bottom
                    if self.player.rect.bottom >= sprite.rect.top and self.player.prev_rect.bottom <= sprite.prev_rect.top:
                        self.player.rect.bottom = sprite.rect.top
                        
                    self.player.direction_vec.y = 0