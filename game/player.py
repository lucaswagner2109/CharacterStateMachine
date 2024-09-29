from .config import Config

import pygame

from pygame.math import Vector2 as vec

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        # Components
        self.input = PlayerInput(self)
        self.movement = PlayerMovement(self)
        
        # Sprite variables                                                 
        self.image = pygame.Surface((32, 32))
        self.image.fill((Config.RED))
        self.rect = self.image.get_frect(center = pos) 
        
        # Movement variables
        self.input_vec = vec()
        
        self.input_disabled = False
        self.speed = Config.PLAYER_WALK_SPEED
        
    def update(self, dt):
        self.input.update()
        self.movement.move(dt)
        
class PlayerInput:
    
    def __init__(self, player):
        self.player = player
        
    def set_input(self):
        self.player.input_vec = vec()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.player.input_vec.x = -1
        elif keys[pygame.K_d]:
            self.player.input_vec.x = 1
        
        if keys[pygame.K_SPACE]:
            self.player.input_vec.y = 1
            
    def update(self):
        if not self.player.input_disabled:
            self.set_input()
            
class PlayerMovement:
    
    def __init__(self, player):
        self.player = player
        self.velocity = vec()
        
    def move(self, dt):

        self.velocity.x = self.player.input_vec.x * Config.PLAYER_RUN_SPEED
        self.player.rect.x += self.velocity.x * dt