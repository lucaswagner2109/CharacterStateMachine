from .config import Config, PlayerStates


import pygame
from pygame.math import Vector2 as vec

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, frames, collision_sprites):
        super().__init__(groups)
        
        # Input
        self.input_disabled = False
        
        # Movement
        self.direction = vec()
        self.velocity = vec()
        
        self.c_sprites = collision_sprites
        
        self.speed = Config.PLAYER_RUN_SPEED
        self.ground = False
        self.crouch = False
        self.jump = False     
         
        # Player state & Animation
        self.states = PlayerStates()
        
        self.state = self.states.IDLE
        self.prev_state = self.states.IDLE
        
        self.facing = "left"
        self.frames = frames
        self.frame_idx = 0
        
        # Sprite
        self.image = frames[self.state.name][self.facing][0]
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,-16)
        
    def input(self):
        input_vec = vec()
        keys = pygame.key.get_pressed()
        # check for horizonal movement
        if keys[pygame.K_a]: 
            input_vec.x = -1
        elif keys[pygame.K_d]:
            input_vec.x = 1
            
        self.jump = True if keys[pygame.K_SPACE] else False
        self.crouch = True if keys[pygame.K_LSHIFT] else False
            
        # set player direction
        self.direction.x = input_vec.normalize().x if input_vec else 0
        
    def move(self, dt):
        # check initial game state
        self.check_contact()
        # get input
        self.input()
        
        ## horizontal movement logic
        self.velocity.x = self.direction.copy().x * self.speed * dt
        self.hitbox.x += self.velocity.x
        self.check_collision("h")
        
        ## vertical movement
        # gravity
        self.velocity.y += Config.GRAVITY * dt
        # jump
        if self.jump and self.ground:
            self.velocity.y = -Config.PLAYER_JUMP_STRENGTH
        
        self.hitbox.y += self.velocity.y * dt
        self.check_collision("v")
        # update player rect according to hitbox movement
        self.rect.center = self.hitbox.center
        
    def check_contact(self):
        ground_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
        # list of rectangles of all collision objects
        collide_rects = [sprite.rect for sprite in self.c_sprites]
        # rect beneath player rectangle
        self.ground = True if ground_rect.collidelist(collide_rects) >= 0 else False
        
    def check_collision(self, axis):
        for sprite in self.c_sprites:
            if sprite.rect.colliderect(self.hitbox):
                # Horizontal collision
                if axis == "h":
                    if self.velocity.x > 0:
                        self.hitbox.right = sprite.rect.left
                    elif self.velocity.x < 0:
                        self.hitbox.left = sprite.rect.right
                        
                    self.velocity.x = 0

                # Vertical collision
                elif axis == "v":
                    if self.velocity.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    elif self.velocity.y < 0:
                        self.hitbox.top = sprite.rect.bottom

                    self.velocity.y = 0
        
    def check_state(self):
        if self.direction.x < 0:
            self.facing = "left"
        elif self.direction.x > 0:
            self.facing = "right"
            
        if self.ground:
            if self.crouch:
                if self.velocity.x == 0:
                    self.state = self.states.CROUCH_IDLE
                else:
                    self.state = self.states.CROUCH_WALK
            else:
                if self.direction.x == 0:
                    self.state = self.states.IDLE
                else:
                    self.state = self.states.RUN
        elif not self.ground:
            if self.velocity.y <= 0:
                self.state = self.states.JUMP
            elif self.velocity.y > 0:
                self.state = self.states.FALL
                
    def animate(self, dt):
        current_frames = self.frames[self.state.name][self.facing]
        if self.state.loop:
            self.frame_idx += self.state.anim_speed * dt   
        else:
            if self.prev_state != self.state:
                self.frame_idx = 0
            else:
                self.frame_idx = self.frame_idx + self.state.anim_speed * dt if self.frame_idx <= len(current_frames) - 1 else self.frame_idx
                
        self.image = current_frames[int(self.frame_idx % len(current_frames))]
        self.prev_state = self.state
        
    def update(self, dt):
        self.input()
        self.move(dt)
        self.check_state()
        self.animate(dt)