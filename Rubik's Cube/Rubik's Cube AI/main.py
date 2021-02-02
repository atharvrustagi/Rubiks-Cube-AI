import pygame as pg
import numpy as np
from cube_utils import *
from os import system

_ = system('cls')

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
solved_state = 0
ang_changed = False
move_counter = 0
error = ""


def draw():
	win.fill(WHITE)
	pg.draw.line(win, BLACK, (WIN_SIZE[1]+50, 0), (WIN_SIZE[1]+50, WIN_SIZE[0]))

	tmp_cube, z = project_surfaces(np.copy(cube))
	dc = {z[x] : x for x in range(54)}
	z.sort()

	for k in reversed(z):
		v = dc[k]
		draw_surface(tmp_cube[v], v)

	draw_color_buttons(win, selected_color)

	global solved_state
	
	if solved_state==0:
		if state<=6:
			draw_prev_next(win)
			if state==1:
				win.blit(state1_ins, (80, 70))
			win.blit(use_arrow_keys, (200, 100))
			# win.blit(next_warning, (WIN_SIZE[1]//2-next_warning.get_width()//2, 130))
		else:
			win.blit(solving_text, (170, 130))
	elif solved_state==1:
		ins_text = font.render("Hold the cube with green face in front and yellow face on top", True, BLACK)
		win.blit(ins_text, (WIN_SIZE[1]//2-ins_text.get_width()//2, 100))
		ins_text = font.render("Click anywhere to take a move", True, BLACK)
		win.blit(ins_text, (WIN_SIZE[1]//2-ins_text.get_width()//2, 70))
		solution_ready_text = font.render("Solution ready!", True, BLACK)
		win.blit(solution_ready_text, (WIN_SIZE[1]//2-solution_ready_text.get_width()//2, 40))
		solution_text = font.render(solution, True, BLACK)
		win.blit(solution_text, (WIN_SIZE[1]//2-solution_text.get_width()//2, 130))

		global ang_changed
		if not ang_changed:
			ang_changed = True
			change_angle()
	else:
		text = font.render(error, True, BLACK)
		win.blit(text, (WIN_SIZE[1]//2-text.get_width()//2, 100))
		win.blit(invalid_text, ((WIN_SIZE[1]//2-invalid_text.get_width()//2, 130)))
		pg.display.update()
		pg.time.delay(2000)
		solved_state = 0

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
	elif solved_state==0:
		if dalpha>1e-3:
			dalpha -= np.pi/2/turn_speed
		elif dalpha<-1e-3:
			dalpha += np.pi/2/turn_speed

		if dbeta>1e-3:
			dbeta -= np.pi/2/turn_speed
		elif dbeta<-1e-3:
			dbeta += np.pi/2/turn_speed

	global selected_color
	if keys[pg.K_w]:
		selected_color = 'w'
	elif keys[pg.K_y]:
		selected_color = 'y'
	elif keys[pg.K_b]:
		selected_color = 'b'
	elif keys[pg.K_g]:
		selected_color = 'g'
	elif keys[pg.K_r]:
		selected_color = 'r'
	elif keys[pg.K_o]:
		selected_color = 'o'

def state_change(os, ns):
	global alpha, beta
	factors = changes(os, ns)
	for _ in range(turn_speed):
		alpha += factors[0]*np.pi/turn_speed/2
		beta += factors[1]*np.pi/turn_speed/2
		draw()

def change_angle():
	global alpha, beta
	for _ in range(turn_speed + turn_speed//3):
		beta -= np.pi/2/turn_speed
		draw()
	for _ in range(turn_speed - turn_speed//3):
		alpha += np.pi/2/turn_speed
		draw()

def play(move):
	moves_to_take = []
	algorithm(move, moves_to_take)
	play_moves(moves_to_take)

def play_moves(moves_to_take, turn_speed=125):
	global alpha, beta
	for x in moves_to_take:
		for _ in range(turn_speed):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()

			turn_face(x, np.pi/turn_speed/2, cube)
			draw()

		turn_face(x, -np.pi/2, cube)
		moves[x](colors)


while True:
	for event in pg.event.get():
		if event.type==pg.QUIT:
			pg.quit()
			exit()
		elif event.type==pg.MOUSEBUTTONDOWN and state<=6:
			pos = pg.mouse.get_pos()
			selected_color, new_state = mouse_action(pos, selected_color, state, colors)
			if state != new_state:
				state_change(state, new_state)
				state = new_state
		elif event.type==pg.MOUSEBUTTONDOWN and solved_state==1 and move_counter < len(sol_list):
			play(sol_list[move_counter])
			move_counter += 1

	keys = pg.key.get_pressed()
	key_action(keys)

	if state>6 and solved_state==0:
		try:
			solution, time = solve_cube(colors)
			sol_list = solution.split(' ')
			print(solution)
			solved_state = 1
		except Exception as e:
			error = str(e)
			print(error)
			state = 6
			solved_state = -1
	elif solved_state==1:
		pass
	draw()

