from .config import Config


import pygame
from pygame.math import Vector2 as vec

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, frames, collision_sprites):
        super().__init__(groups)
        
        # Input control
        self.input_disabled = False
        
        # Player state
        self.state = "idle"    
        self.facing = "right"

        self.image = frames[self.state][self.facing][0]
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.inflate(-32,-16)
        
        # Components
        self.movement = PlayerMovement(self, collision_sprites)
        self.animation = PlayerAnimation(self, frames)

    def update(self, dt):
        self.prev_rect = self.rect.copy()
        
        self.movement.move(dt)
        self.animation.animate(dt)
    
class PlayerMovement:
    
    def __init__(self, player, collision_sprites):
        self.player = player
        self.collision_sprites = collision_sprites
        
        self.hitbox = self.player.hitbox
        
        self.speed = Config.PLAYER_RUN_SPEED
        self.direction = vec()
        self.velocity = vec()
        
        self.ground = False
        self.crouch = False
        
        self.jump = False
        
        self.facing = "right"
        self.state = "idle"
        
    def check_contact(self):
        ground_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
        # list of rectangles of all collision objects
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        # rect beneath player rectangle
        self.ground = True if ground_rect.collidelist(collide_rects) >= 0 else False
        
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
        
    def check_collision(self, axis):
        for sprite in self.collision_sprites:
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
                    
    def states(self):
        if self.direction.x < 0:
            self.facing = "left"
        elif self.direction.x > 0:
            self.facing = "right"
            
        if self.ground:
            if self.crouch:
                self.state = "crouch"
            elif self.jump:
                self.state = "jump"
            else:
                if self.direction.x == 0:
                    self.state = "idle"
                else:
                    self.state = "run"
        elif not self.ground:
            if self.velocity.y <= 0:
                self.state = "jump"
            elif self.velocity.y > 0:
                self.state = "fall"
        
    def set_state(self):
        self.player.facing = self.facing
        self.player.state = self.state
        
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
        
        self.states()
        self.set_state()
        # update player rect according to hitbox movement
        self.player.rect.center = self.hitbox.center
                       
class PlayerAnimation:
    
    def __init__(self, player, frames):
        self.player = player
        self.frames = frames
        self.frame_idx = 0
        
        self.animation_speed = Config.ANIMATION_SPEED
        
        self.prev_state = "idle"
        self.one_time_states = ["jump", "fall"]
        
    def animate(self, dt):
        state, facing = self.player.state, self.player.facing
        image = self.player.image
        if state == self.prev_state and state in self.one_time_states:
            pass
            
        else:
            self.frame_idx += self.animation_speed * dt
            current_frames = self.frames[state][facing]
            image = current_frames[int(self.frame_idx % len(current_frames))]
        
        self.prev_state = state
        self.player.image = image