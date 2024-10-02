import pygame

from os.path import join
from os import walk

def import_image(*path, alpha = True, format = 'png'):
    file_path = join(*path) + f'.{format}'
    if alpha:
        surface = pygame.image.load(file_path).convert_alpha()
    else:
        surface = pygame.image.load(file_path).convert()
    return surface

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = import_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height), pygame.SRCALPHA).convert_alpha()
			cutout_surf.blit(surf, (0,0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames