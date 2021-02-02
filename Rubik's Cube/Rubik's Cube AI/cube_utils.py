import pygame as pg
import numpy as np
import kociemba as kc
from time import perf_counter as pf
from Cube_functions import *


# clrs = {0:(255, 0, 38), 1:(36, 255, 50), 2:(255, 238, 0), 3:(255, 100, 0), 4:(21, 113, 243), 5:(255, 255, 255)}
RED = (255, 0, 38)
GREEN = (36, 255, 50)
YELLOW = (255, 238, 0)
ORANGE = (255, 100, 0)
BLUE = (21, 113, 243)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def changes(os, ns):
	if os==1 and ns==2:
		return (0, 1)
	if os==2 and ns==1:
		return (0, -1)
	if os==2 and ns==3:
		return (1, 0)
	if os==3 and ns==2:
		return (-1, 0)
	if os==3 and ns==4:
		return (1, 0)
	if os==4 and ns==3:
		return (-1, 0)
	if os==4 and ns==5:
		return (1, 0)
	if os==5 and ns==4:
		return (-1, 0)
	if os==5 and ns==6:
		return (0, 1)
	if os==6 and ns==5:
		return (0, -1)
	if ns==7:
		return (0, 0)

def create_cube(side = 50):
	s = side
	surfaces = np.zeros((6, 3, 3, 4, 3))	# 6 faces, 3x3 squares each, 4 (x,y,z) coordinates for each squares
	# left face, centre
	surfaces[0, 1, 1] = np.array([[-3*s, -s, s], [-3*s, -s, -s], [-3*s, s, -s], [-3*s, s, s]])
	# front face, centre
	surfaces[1, 1, 1] = np.array([[-s, s, -3*s], [-s, -s, -3*s], [s, -s, -3*s], [s, s, -3*s]])
	# top face, centre
	surfaces[2, 1, 1] = np.array([[-s, -3*s, -s], [-s, -3*s, s], [s, -3*s, s], [s, -3*s, -s]])

	for i in range(3):
		for j in range(3):
			# left face
			surfaces[0, i, j] = surfaces[0, 1, 1]
			surfaces[0, i, j, :, 2] -= (i-1)*2*s
			surfaces[0, i, j, :, 1] += (j-1)*2*s

			# front face
			surfaces[1, i, j] = surfaces[1, 1, 1]
			surfaces[1, i, j, :, 0] += (i-1)*2*s
			surfaces[1, i, j, :, 1] += (j-1)*2*s

			# top face
			surfaces[2, i, j] = surfaces[2, 1, 1]
			surfaces[2, i, j, :, 0] += (i-1)*2*s
			surfaces[2, i, j, :, 2] -= (j-1)*2*s

	# right face
	surfaces[3] = surfaces[0]
	surfaces[3, ..., 0] += 6*s
	surfaces[3, ..., 2] *= -1

	# back face
	surfaces[4] = surfaces[1]
	surfaces[4, ..., 2] += 6*s
	surfaces[4, ..., 0] *= -1

	# bottom face
	surfaces[5] = surfaces[2]
	surfaces[5, ..., 1] += 6*s
	surfaces[5, ..., 0] *= -1

	return surfaces

def create_params(W, theta, Zv):
	return W/np.tan(theta/2), Zv


clrs = {'r':(255, 0, 38), 'g':(36, 255, 50), 'y':(255, 238, 0), 
		'o':(255, 100, 0), 'b':(21, 113, 243), 'w':(255, 255, 255)}

clrs_rev = {np.sum(clrs[k]):k for k in clrs.keys()}

def init_colors():
	colors = np.zeros((54, 3), dtype=np.uint8)
	for i, k in enumerate(clrs.keys()):
		colors[i*9:i*9+9] = clrs[k]
	return colors

color_buttons = {'r':np.array([850, 300]), 'g':np.array([850, 350]), 'b':np.array([850, 400]),
				 'o':np.array([850, 450]), 'y':np.array([850, 500]), 'w':np.array([850, 550])}

# color button
button_size = 50

pg.font.init()
font = pg.font.SysFont("georgia", 20)

state1_ins = font.render("Hold the Cube with Yellow face in front and Blue face on top", True, BLACK)
use_arrow_keys = font.render("Use Arrow keys to scout the cube", True, BLACK)
next_warning = font.render("If the 'Next' button doesn't work, the colors are invalid", True, BLACK)
solving_text = font.render("Solving... (this will take at max 10 seconds)", True, BLACK)
invalid_text = font.render("Invalid cube state. Verify the colors", True, BLACK)
np_width = 150
np_height = 75
prev_text = font.render("Previous", True, WHITE)
next_text = font.render("Next", True, WHITE)
np_coors = np.array([[100, 600], [500, 600]])

def draw_prev_next(win):
	pg.draw.rect(win, BLACK, (np_coors[0, 0], np_coors[0, 1], np_width, np_height))
	pg.draw.rect(win, BLACK, (np_coors[1, 0], np_coors[1, 1], np_width, np_height))
	win.blit(prev_text, (np_coors[0, 0]+np_width//2-prev_text.get_width()//2,
			 np_coors[0, 1]+np_height//2-prev_text.get_height()//2))
	win.blit(next_text, (np_coors[1, 0]+np_width//2-next_text.get_width()//2,
			 np_coors[1, 1]+np_height//2-next_text.get_height()//2))

def draw_color_buttons(win, s):
	for k in color_buttons.keys():
		pg.draw.rect(win, clrs[k], (color_buttons[k][0], 
			color_buttons[k][1], button_size, button_size))
	pg.draw.rect(win, (75, 75, 75), (847, 297, button_size+5, 6*button_size+5), 5)
	pg.draw.rect(win, BLACK, (color_buttons[s][0]-3, 
			color_buttons[s][1]-3, button_size+5, button_size+5), 5)

"""
input:
yellow - green - orange - blue - red - white

solving:
# green - front
# yellow - top

cube start -> (225, 255)
cube mid1  -> (308, 308)
cube mid2  -> (392, 392)
cube end   -> (475, 475)

"""

pos_list = [225, 308, 392, 475]

state_color_list = np.array([[i for i in range(18, 27)],
							 [i for i in range(9, 18)],
							 [i for i in range(27, 36)],
							 [i for i in range(36, 45)],
							 [i for i in range(9)],
							 [51,48,45,52,49,46,53,50,47]])

def change_color(colors, pos, scolor, state):
	# print("clicked")
	for i in range(len(pos_list)-1):
		if pos_list[i] <= pos[0] <= pos_list[i+1]:
			for j in range(len(pos_list)-1):
				if pos_list[j] <= pos[1] <= pos_list[j+1] and (i!=1 or j!=1):
					colors[state_color_list[state, i*3+j]] = clrs[scolor]

def mouse_action(pos, scolor, state, colors):
	# cube input
	if (225 < pos[0] < 475) and (225 < pos[1] < 475):
		change_color(colors, pos, scolor, state-1)
		return scolor, state

	# previous next
	if np_coors[0, 1] <= pos[1] <= np_coors[0, 1] + np_height:
		if np_coors[0, 0] <= pos[0] <= np_coors[0, 0] + np_width:			
			return scolor, (state-1) if state>1 else 1
		elif np_coors[1, 0] <= pos[0] <= np_coors[1, 0] + np_width:		
			return scolor, (state+1)# if state<6 else state

	# color selection
	if 850 <= pos[0] <= 900:
		for k in color_buttons.keys():
			if color_buttons[k][1] <= pos[1] <= color_buttons[k][1] + 50:
				return k, state
	return scolor, state

def solve_cube(colors):
	t = pf()
	s = color_to_str(colors)
	sol = kc.solve(s)
	return sol, pf()-t

def color_to_str(colors):
	s = ""
	for c in colors[[18,21,24,19,22,25,20,23,26]]:
		s += clrs_rev[np.sum(c)]

	for c in colors[[27,30,33,28,31,34,29,32,35]]:
		s += clrs_rev[np.sum(c)]

	for c in colors[[9,12,15,10,13,16,11,14,17]]:
		s += clrs_rev[np.sum(c)]

	for c in colors[[53,50,47,52,49,46,51,48,45]]:
		s += clrs_rev[np.sum(c)]

	for c in colors[[0,3,6,1,4,7,2,5,8]]:
		s += clrs_rev[np.sum(c)]

	for c in colors[[36,39,42,37,40,43,38,41,44]]:
		s += clrs_rev[np.sum(c)]

	# mapping
	ns = ""
	for c in s:
		if c=='y':
			ns += 'U'
		elif c=='g':
			ns += 'F'
		elif c=='r':
			ns += 'L'
		elif c=='o':
			ns += 'R'
		elif c=='w':
			ns += 'D'
		elif c=='b':
			ns += 'B'

	# print(s)
	# print(ns)
	return ns

def algorithm(move, moves_to_take):
	l = move
	if len(l) > 1 and l[1]=='2':
		for _ in range(2):
			x = algo_move[l[0]]
			moves_to_take.append(x)
	else:
		x = algo_move[l]
		moves_to_take.append(x)

