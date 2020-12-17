import pygame as pg
import numpy as np
from time import perf_counter as pf
from Cube_functions import *


run = True
W = 1000
theta = np.pi/2
t = np.tan(theta/2)
zn = 10
zf = 1000
Z = (zn+zf)/2
L = 2*Z*t
win = pg.display.set_mode((W, W))
pg.font.init()
font = pg.font.SysFont("georgia", 20)


# creating the cube
s = 50		# size of each cube
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
	for i in range(30):
		x = np.random.randint(0, 12)
		for _ in range(turn_speed):
			turn_face(x, np.pi/turn_speed/2, surfaces)
			draw()
		turn_face(x, -np.pi/2, surfaces)
		moves[x](colors)
		taken.append(x)
		draw()
	print()

def solve():
	print()
	global alpha, beta
	for x in taken[::-1]:
		if x==12:
			moves[12](1, colors)
			alpha -= np.pi/2
		elif x==13:
			moves[12](0, colors)
			alpha += np.pi/2
		else:
			for _ in range(turn_speed):
				turn_face(x, np.pi/turn_speed/2, surfaces)
				draw()
			turn_face(x, -np.pi/2, surfaces)
			moves[(x+6)%12](colors)
		draw()
	taken.clear()
	print()

def undo():
	return
	# for m in reversed(taken):
	# 	if m < 12:
	# 		taken.remove(m)
	# 		moves[(m+6)%12]()
	# 		break

def check_solve():
	for i in range(6):
		for j in range(8):
			if np.sum(colors[i*9+j] - colors[i*9+j+1])==0:
				continue
			else:
				return False
	return True


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
	# t = font.render(str(v), True, (0,0,0))
	# win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))
	
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
	for i, s in enumerate(instructions):
		t = font.render(s, True, clrs[5])
		win.blit(t, (10, 10+i*25))

	global fps_disp
	fps_text = font.render("FPS: " + str(fps_disp), True, (255, 255, 255))
	win.blit(fps_text, (W-fps_text.get_width()-10, fps_text.get_height()+10))

	if pf()%1<0.01:
		fps_disp = round(1/(pf()-fps))
		win.blit(fps_text, (W-fps_text.get_width()-10, fps_text.get_height()+10))

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

	k = (L/(L + cube[..., 2]*t)).reshape(6, 3, 3, 4, 1)		# perspective factor
	z = np.mean(cube[..., 2], axis=3).reshape(54)
	
	return W//2 + (k*cube[..., :2]).reshape(54, 4, 2), z


alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01	# default viewing angles
inc = 0.02										# angle increase on pressing arrow keys
fps = 0											# frames per second
timer = 0										# counts frames elapsed per turn
turn_speed = 25									# less is more (it is actually the number of frames spent per turn)
wait = 150										# wait (in msec) after some functions
interval = p_interval = 0						# for changing front-face on rotation
fps_disp = 0

instructions = ["Rotate cube: Arrow Keys", "Shuffle: SHIFT + S", "Solve: CTRL + S", "Moves (clockwise): F B R L D B", "Moves (anti-clockwise): SHIFT + (F B R L D B)"]
for i in instructions:
	print(i)

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
		n = move_to_play(keyp)
		if n>=0:
			timer = 1


	if keyp[pg.K_s] and keyp[pg.K_LSHIFT]:
		shuffle()
		pg.time.delay(wait)
	elif keyp[pg.K_LCTRL] or keyp[pg.K_RCTRL]:
		if keyp[pg.K_s]:
			solve()
			# alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01
		elif keyp[pg.K_z]:
			undo()

	fps = pf()

	if timer>0:
		turn_face(n, np.pi/turn_speed/2, surfaces)
		timer += 1
		if timer == turn_speed+1:
			timer = 0
			turn_face(n, -np.pi/2, surfaces)
			surfaces = np.rint(surfaces)
			taken.append(n)
			moves[n](colors)
	
	if alpha > 2*np.pi or alpha < -2*np.pi:
		alpha = 0
	if beta > np.pi/2:
		beta = np.pi/2 + 0.01
	if beta < -np.pi/2:
		beta = -np.pi/2 + 0.01

	interval = int(2*(alpha+(1 if alpha>0 else -1)*np.pi/4)/np.pi)%4
	if interval>p_interval:
		change_front(0, colors)
		alpha += np.pi/2
		taken.append(12)
	
	draw()


""" 
to add:
	undo
	redo
	AI to solve
"""
