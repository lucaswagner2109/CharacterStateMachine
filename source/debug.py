import pygame
from .config import Config

def draw_info(info, screen):
    font = pygame.font.Font("assets/fonts/pokemon-ds-font.ttf", 32)
    info = str(info)
    info_text = font.render(info, True, Config.WHITE)
    info_rect = info_text.get_frect(topleft = (12, 12))
    screen.blit(info_text, info_rect)
    
def draw_hitbox(screen, pos, size):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surf, Config.RED + (128,), surf.get_rect(), 1)
    screen.blit(surf, pos)