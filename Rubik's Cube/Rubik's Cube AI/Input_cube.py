import pygame as pg
import numpy as np
from cube_utils import *
# import kociemba
# from draw_utils import *

WIN_SIZE = (1000, 700)
win = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption("Cube")

cube = create_cube(50)		# cube with side = 50
colors = init_colors()

# field of view params
f, Zv = create_params(WIN_SIZE[1], theta=np.pi/2, Zv=1000)
turn_speed = 100
alpha, beta = 1e-3, -np.pi/2 + 1e-3
dalpha, dbeta = 0, 0
selected_color = 'r'
state = 1
solved = False


def draw(win):
	win.fill(WHITE)
	pg.draw.line(win, BLACK, (WIN_SIZE[1]+50, 0), (WIN_SIZE[1]+50, WIN_SIZE[0]))

	tmp_cube, z = project_surfaces(np.copy(cube))
	dc = {z[x] : x for x in range(54)}
	z.sort()

	for k in reversed(z):
		v = dc[k]
		draw_surface(tmp_cube[v], v)

	draw_color_buttons(win, selected_color)
	
	if state<6:
		draw_prev_next(win)
		if state==1:
			win.blit(state1_ins, (80, 100))
		win.blit(use_arrow_keys, (200, 130))
	else:
		win.blit(solving_text, (180, 100))

	pg.display.update()

def draw_surface(s, v):
	# s -> 4, 2-D coordinates in cyclic order
	pg.draw.polygon(win, colors[v], s)
	for i in range(3):
		pg.draw.line(win, (32, 32, 32), s[i], s[i+1], 3)
	pg.draw.line(win, (32, 32, 32), s[0], s[3], 3)
	# index of each square
	# t = font.render(str(v), True, (0,0,0))
	# win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))

def project_surfaces(cube):
	h = (cube[..., 0]**2 + cube[..., 2]**2)**0.5
	a = np.arctan(cube[..., 2]/(cube[..., 0] + 1e-8)) - (alpha+dalpha)
	c = np.where(cube[..., 0]>=0, 1, -1)
	cube[..., 0] = c*h*np.cos(a)
	cube[..., 2] = c*h*np.sin(a)

	h = (cube[..., 1]**2 + cube[..., 2]**2)**0.5
	a = np.arctan(cube[..., 2]/(cube[..., 1] + 1e-8)) - (beta+dbeta)
	c = np.where(cube[..., 1]>=0, 1, -1)
	cube[..., 1] = c*h*np.cos(a)
	cube[..., 2] = c*h*np.sin(a)

	z = np.mean(cube[..., 2], axis=3).reshape(54)
	return WIN_SIZE[1]//2 + (f*cube[..., :2]/(Zv+cube[..., 2:])).reshape(54, 4, 2), z

def key_action(keys):
	global alpha, beta, dalpha, dbeta
	if keys[pg.K_UP] and dbeta <= np.pi/2:
		dbeta += np.pi/2/turn_speed
	elif keys[pg.K_DOWN] and dbeta >= -np.pi/2:
		dbeta -= np.pi/2/turn_speed
	elif keys[pg.K_LEFT] and dalpha <= np.pi/2:
		dalpha += np.pi/2/turn_speed
	elif keys[pg.K_RIGHT] and dalpha >= -np.pi/2:
		dalpha -= np.pi/2/turn_speed
	else:
		if dalpha>1e-3:
			dalpha -= np.pi/2/turn_speed
		elif dalpha<-1e-3:
			dalpha += np.pi/2/turn_speed

		if dbeta>1e-3:
			dbeta -= np.pi/2/turn_speed
		elif dbeta<-1e-3:
			dbeta += np.pi/2/turn_speed

def state_change(os, ns):
	global alpha, beta
	factors = changes(os, ns)
	for _ in range(turn_speed):
		alpha += factors[0]*np.pi/turn_speed/2
		beta += factors[1]*np.pi/turn_speed/2
		draw(win)


while True:
	for event in pg.event.get():
		if event.type==pg.QUIT:
			pg.quit()
			exit()
		elif event.type==pg.MOUSEBUTTONDOWN and state<6:
			pos = pg.mouse.get_pos()
			selected_color, new_state = mouse_action(pos, selected_color, state, colors)
			if state != new_state:
				state_change(state, new_state)
				state = new_state

	keys = pg.key.get_pressed()
	key_action(keys)
	draw(win)

	if state>=6 and not solved:
		try:
			solution, time = solve_cube(colors)
			print(solution)
			solved = True
		except:
			print("Invalid cube. Enter again")
			state = 5

