import pygame as pg
import numpy as np
from time import perf_counter as pf
from Cube_functions import *
from os import system
from AI import *

_ = system("cls")


def play(moves_to_take):
	global alpha, beta
	for x in moves_to_take:
		if x<12:
			for _ in range(turn_speed):
				for event in pg.event.get():
					if event.type == pg.QUIT:
						exit()

				keyp = pg.key.get_pressed()
				if keyp[pg.K_UP]:
					beta += inc
				elif keyp[pg.K_DOWN]:
					beta -= inc
				if keyp[pg.K_LEFT]:
					alpha += inc
				elif keyp[pg.K_RIGHT]:
					alpha -= inc
				if alpha > 2*np.pi or alpha < -2*np.pi:
					alpha = 0
				if beta > np.pi/2:
					beta = np.pi/2 + 0.01
				if beta < -np.pi/2:
					beta = -np.pi/2 + 0.01

				turn_face(x, np.pi/turn_speed/2, surfaces)
				draw()
			turn_face(x, -np.pi/2, surfaces)
			moves[x](colors)
		elif x==12:
			change_front(0, colors)
			alpha += np.pi/2
		elif x==13:
			change_front(1, colors)
			alpha -= np.pi/2


def cross():
	s_cube = np.copy(colors)

	moves_to_take = []

	while not np.all(s_cube[46:53:2]==255):
		# identifying white edge piece
		idx = -1
		for i, c in enumerate(s_cube[:45]):
			if (i%9)%2==1 and np.all(c==255):
				idx = i
				break


		# if white edge piece is on the sides
		if (idx>=0 and idx<18) or (idx>=27 and idx<45):
			# identifying which face to switch to
			face = -1
			for i, l in enumerate(side_face_list):
				if idx>=l[0] and idx<l[1]:
					face = i
					break

			if face==0:
				change_front(0, s_cube)
				moves_to_take.append(12)
			elif face==2:
				change_front(1, s_cube)
				moves_to_take.append(13)
			elif face==3:
				change_front(0, s_cube)
				moves_to_take.append(12)
				change_front(0, s_cube)
				moves_to_take.append(12)

			# checking if the move to take is already occupied
			fidx = (idx%9)+9
			if fidx==10:
				while np.all(s_cube[52]==255):
					fd(s_cube)
					moves_to_take.append(1)
				fl(s_cube)
				moves_to_take.append(2)
			elif fidx==16:
				while np.all(s_cube[46]==255):
					fd(s_cube)
					moves_to_take.append(1)
				fr_(s_cube)
				moves_to_take.append(9)
			elif fidx==12:
				while np.all(s_cube[50]==255):
					fd(s_cube)
					moves_to_take.append(1)
				ff(s_cube)
				fd(s_cube)
				fr_(s_cube)
				moves_to_take.append(4)
				moves_to_take.append(1)
				moves_to_take.append(9)
			elif fidx==14:
				while np.all(s_cube[50]==255):
					fd(s_cube)
					moves_to_take.append(1)
				ff_(s_cube)
				fd(s_cube)
				fr_(s_cube)
				moves_to_take.append(10)
				moves_to_take.append(1)
				moves_to_take.append(9)


		# if white edge piece is on the top face
		else:
			if idx==23:
				while np.all(s_cube[50]==255):
					fd(s_cube)
					moves_to_take.append(1)
				ff(s_cube)
				ff(s_cube)
				moves_to_take.append(4)
				moves_to_take.append(4)
			elif idx==25:
				while np.all(s_cube[46]==255):
					fd(s_cube)
					moves_to_take.append(1)
				fr(s_cube)
				fr(s_cube)
				moves_to_take.append(3)
				moves_to_take.append(3)
			elif idx==21:
				while np.all(s_cube[48]==255):
					fd(s_cube)
					moves_to_take.append(1)
				fb(s_cube)
				fb(s_cube)
				moves_to_take.append(5)
				moves_to_take.append(5)
			elif idx==19:
				while np.all(s_cube[52]==255):
					fd(s_cube)
					moves_to_take.append(1)
				fl(s_cube)
				fl(s_cube)
				moves_to_take.append(2)
				moves_to_take.append(2)

	return moves_to_take


def AI():
	global alpha, beta
	moves_to_take = cross()
	play(moves_to_take)






run = True
W = 1000
theta = np.pi/2
Zv = 1000
f = W/np.tan(theta/2)
win = pg.display.set_mode((W, W))
pg.display.set_caption("Rubik's Cube")
pg.font.init()
font = pg.font.SysFont("georgia", 20)



# creating the cube
s = 50		# size of each small cube
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


taken = []

"""
initial parameters:
0 -> left, red
1 -> front, green
2 -> top, yellow
3 -> right, orange
4 -> back, blue
5 -> bottom, white
"""

clrs = {0:(255, 0, 38), 1:(36, 255, 50), 2:(255, 238, 0), 3:(255, 100, 0), 4:(21, 113, 243), 5:(255, 255, 255)}
colors = np.zeros((54, 3))
for i in clrs.keys():
	colors[i*9:i*9+9] = clrs[i]


def shuffle():
	global alpha, beta
	for i in range(25):
		x = np.random.randint(0, 12)
		for _ in range(turn_speed):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()

			keyp = pg.key.get_pressed()
			if keyp[pg.K_UP]:
				beta += inc
			elif keyp[pg.K_DOWN]:
				beta -= inc
			if keyp[pg.K_LEFT]:
				alpha += inc
			elif keyp[pg.K_RIGHT]:
				alpha -= inc
			if alpha > 2*np.pi or alpha < -2*np.pi:
				alpha = 0
			if beta > np.pi/2:
				beta = np.pi/2 + 0.01
			if beta < -np.pi/2:
				beta = -np.pi/2 + 0.01

			turn_face(x, np.pi/turn_speed/2, surfaces)
			draw()
		turn_face(x, -np.pi/2, surfaces)
		moves[x](colors)
		taken.append(x)

		draw()
	print()

# drawing
def draw_surface(s, v):
	# s -> 4, 2-D coordinates in cyclic order
	pg.draw.polygon(win, colors[v], s)
	for i in range(3):
		pg.draw.line(win, (32, 32, 32), s[i], s[i+1], 6)
	pg.draw.line(win, (32, 32, 32), s[0], s[3], 6)
	if v==13:
		t = font.render("Front", True, (0,0,0))
		win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))
	if v==22:
		t = font.render("Up", True, (0,0,0))
		win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))
	t = font.render(str(v), True, (0,0,0))
	win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))
	
def draw():
	win.fill((0, 0, 0))
	cube, z = project_surfaces(np.copy(surfaces))

	dc = dict()
	for x in range(54):
		dc[z[x]] = x
	z.sort()

	for k in reversed(z):
		v = dc[k]
		draw_surface(cube[v], v)

	pg.display.update()

def project_surfaces(cube):
	h = (cube[..., 0]**2 + cube[..., 2]**2)**0.5
	a = np.arctan(cube[..., 2]/(cube[..., 0] + 1e-8)) - alpha
	c = np.where(cube[..., 0]>=0, 1, -1)
	cube[..., 0] = c*h*np.cos(a)
	cube[..., 2] = c*h*np.sin(a)

	h = (cube[..., 1]**2 + cube[..., 2]**2)**0.5
	a = np.arctan(cube[..., 2]/(cube[..., 1] + 1e-8)) - beta
	c = np.where(cube[..., 1]>=0, 1, -1)
	cube[..., 1] = c*h*np.cos(a)
	cube[..., 2] = c*h*np.sin(a)

	# k = (L/(L + cube[..., 2]*t)).reshape(6, 3, 3, 4, 1)		# perspective factor
	z = np.mean(cube[..., 2], axis=3).reshape(54)
	
	return W//2 + (f*cube[..., :2]/(Zv+cube[..., 2:])).reshape(54, 4, 2), z


alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01				# default viewing angles
inc = 0.02													# angle increase on pressing arrow keys
fps = 0														# frames per second
timer = 0													# counts frames elapsed per turn
turn_speed = 25												# MUST BE A POWER OF 5 (5, 25, 125, 625...), less is more (it is actually the number of frames spent per turn)
wait = 150													# wait (in msec) after some functions
interval = p_interval = 0									# for changing front-face on rotation

while run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
	keyp = pg.key.get_pressed()

	if keyp[pg.K_UP]:
		beta += inc
	elif keyp[pg.K_DOWN]:
		beta -= inc
	if keyp[pg.K_LEFT]:
		alpha += inc
	elif keyp[pg.K_RIGHT]:
		alpha -= inc

	if timer==0:
		n = -1		# move_to_play(colors)
		if n>=0:
			timer = 1

	if keyp[pg.K_s] and (keyp[pg.K_LSHIFT]or keyp[pg.K_RSHIFT]):
		shuffle()
		pg.time.delay(wait)

	if keyp[pg.K_s] and (keyp[pg.K_LCTRL] or keyp[pg.K_RCTRL]):
		AI()
		pg.time.delay(500)

	fps = pf()

	if timer>0:
		turn_face(n, np.pi/turn_speed/2, surfaces)
		timer += 1
		if timer == turn_speed+1:
			timer = 0
			turn_face(n, -np.pi/2, surfaces)
			surfaces = np.round(surfaces, -1)
			taken.append(n)
			moves[n](colors)
	
	if alpha > 2*np.pi or alpha < -2*np.pi:
		alpha = 0
	if beta > np.pi/2:
		beta = np.pi/2 + 0.01
	if beta < -np.pi/2:
		beta = -np.pi/2 + 0.01


	draw()

	# if pf()%1 < 0.01:
	# 	print(f"FPS: {round(1/(pf()-fps))}")


""" 
to add:
	undo
	redo
	AI to solve
"""
