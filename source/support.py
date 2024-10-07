import pygame

from os.path import join
from os import listdir

def import_image(path, alpha = True):
	if alpha:
		surface = pygame.image.load(path).convert_alpha()
	else:
		surface = pygame.image.load(path).convert()
	return surface

def import_sprites_folder(path):
	# create output dict
	frame_dict = {}
	frame_width, frame_height = (48, 48)
	# iterate over files
	pngs = [f for f in listdir(path) if f.endswith('.png')] 
	for png in pngs:
		sprite_sheet = import_image(join(path) + "/" + png)
		# cal n columns
		width, height = sprite_sheet.get_size()
		n_cols = width // frame_width
		# create left / right dict
		lr_dict = {"left": [], "right": []}
		# extract frames from sheet
		for c in range(n_cols):
			# get right frame from first row
			right_frame = sprite_sheet.subsurface(pygame.Rect(c * frame_width, 0, frame_width, frame_height))
			lr_dict["right"].append(right_frame)
			# get left frame from second row
			left_frame = sprite_sheet.subsurface(pygame.Rect(c * frame_width, frame_height, frame_width, frame_height))
			lr_dict["left"].append(left_frame)
		# store lr_dict under action name in output dict
		action = png.split(".")[0]
		frame_dict[action] = lr_dict
	return frame_dict
		