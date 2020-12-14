import pygame as pg
import numpy as np
from time import perf_counter as pf


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

lists = [[i for i in range(9)], [i for i in range(9, 18)], [i for i in range(27, 36)], [i for i in range(36, 45)]]

def change_front(face):
	global alpha, beta
	if face==0:
		colors[lists[0]+lists[1]+lists[2]+lists[3]] = colors[lists[3]+lists[0]+lists[1]+lists[2]]
		colors[[18,19,20,23,26,25,24,21]] = colors[[24,21,18,19,20,23,26,25]]
		colors[[53,50,47,46,45,48,51,52]] = colors[[51,52,53,50,47,46,45,48]]
		alpha += np.pi/2
	else:
		colors[lists[0]+lists[1]+lists[2]+lists[3]] = colors[lists[1]+lists[2]+lists[3]+lists[0]]
		colors[[18,19,20,23,26,25,24,21]] = colors[[20,23,26,25,24,21,18,19]]
		colors[[53,50,47,46,45,48,51,52]] = colors[[47,46,45,48,51,52,53,50]]
		alpha -= np.pi/2


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


# cube functions (moves)
# f (before every move name) means fast lol
def fu():
	colors[[0,3,6,9,12,15,27,30,33,36,39,42]] = colors[[9,12,15,27,30,33,36,39,42,0,3,6]]
	colors[[18,19,20,23,26,25,24,21]] = colors[[20,23,26,25,24,21,18,19]]
	print("U", end=' ')

def fu_():
	colors[[0,3,6,9,12,15,27,30,33,36,39,42]] = colors[[36,39,42,0,3,6,9,12,15,27,30,33]]
	colors[[18,19,20,23,26,25,24,21]] = colors[[24,21,18,19,20,23,26,25]]
	print("U'", end=' ')

def fd():
	colors[[2,5,8,11,14,17,29,32,35,38,41,44]] = colors[[38,41,44,2,5,8,11,14,17,29,32,35]]
	colors[[53,50,47,46,45,48,51,52]] = colors[[51,52,53,50,47,46,45,48]]
	print("D", end=' ')

def fd_():
	colors[[2,5,8,11,14,17,29,32,35,38,41,44]] = colors[[11,14,17,29,32,35,38,41,44,2,5,8]]
	colors[[53,50,47,46,45,48,51,52]] = colors[[47,46,45,48,51,52,53,50]]
	print("D'", end=' ')

def fl():
	colors[[18,19,20,9,10,11,53,52,51,44,43,42]] = colors[[44,43,42,18,19,20,9,10,11,53,52,51]]
	colors[[0,1,2,5,8,7,6,3]] = colors[[2,5,8,7,6,3,0,1]]
	print("L", end=' ')

def fl_():
	colors[[18,19,20,9,10,11,53,52,51,44,43,42]] = colors[[9,10,11,53,52,51,44,43,42,18,19,20]]
	colors[[0,1,2,5,8,7,6,3]] = colors[[6,3,0,1,2,5,8,7]]
	print("L'", end=' ')

def fr():
	colors[[24,25,26,15,16,17,47,46,45,38,37,36]] = colors[[15,16,17,47,46,45,38,37,36,24,25,26]]
	colors[[27,28,29,32,35,34,33,30]] = colors[[29,32,35,34,33,30,27,28]]
	print("R", end=' ')

def fr_():
	colors[[24,25,26,15,16,17,47,46,45,38,37,36]] = colors[[38,37,36,24,25,26,15,16,17,47,46,45]]
	colors[[27,28,29,32,35,34,33,30]] = colors[[33,30,27,28,29,32,35,34]]
	print("R'", end=' ')

def ff():
	colors[[6,7,8,53,50,47,29,28,27,26,23,20]] = colors[[53,50,47,29,28,27,26,23,20,6,7,8]]
	colors[[9,10,11,14,17,16,15,12]] = colors[[11,14,17,16,15,12,9,10]]
	print("F", end=' ')

def ff_():
	colors[[6,7,8,53,50,47,29,28,27,26,23,20]] = colors[[26,23,20,6,7,8,53,50,47,29,28,27]]
	colors[[9,10,11,14,17,16,15,12]] = colors[[15,12,9,10,11,14,17,16]]
	print("F'", end=' ')

def fb():
	colors[[0,1,2,51,48,45,35,34,33,24,21,18]] = colors[[24,21,18,0,1,2,51,48,45,35,34,33]]
	colors[[36,37,38,41,44,43,42,39]] = colors[[38,41,44,43,42,39,36,37]]
	print("B", end=' ')

def fb_():
	colors[[0,1,2,51,48,45,35,34,33,24,21,18]] = colors[[51,48,45,35,34,33,24,21,18,0,1,2]]
	colors[[36,37,38,41,44,43,42,39]] = colors[[42,39,36,37,38,41,44,43]]
	print("B'", end=' ')


moves = {0:fu, 1:fd, 2:fl, 3:fr, 4:ff, 5:fb, 6:fu_, 7:fd_, 8:fl_, 9:fr_, 10:ff_, 11:fb_, 12:change_front}
taken = []

def shuffle():
	for i in range(30):
		x = np.random.randint(0, 12)
		moves[x]()
		taken.append(x)
		draw()
	print()

def solve():
	print()
	for x in reversed(taken):
		if x==12:
			moves[12](1)
		elif x==13:
			moves[12](0)
		else:
			moves[(x+6)%12]()
		draw()
	taken.clear()
	print()

def undo():
	pass

# animations
def u_animate(ang):
	# rotates top face by the given angle
	h = (surfaces[[0, 1, 3, 4], :, 0, :, 0]**2 + surfaces[[0, 1, 3, 4], :, 0, :, 2]**2)**0.5
	a = np.arctan(surfaces[[0, 1, 3, 4], :, 0, :, 2] / (surfaces[[0, 1, 3, 4], :, 0, :, 0] + 1e-8))
	c = np.where(surfaces[[0, 1, 3, 4], :, 0, :, 0]>=0, 1, -1)
	a -= ang
	surfaces[[0, 1, 3, 4], :, 0, :, 0] = c*h*np.cos(a)
	surfaces[[0, 1, 3, 4], :, 0, :, 2] = c*h*np.sin(a)

	h = (surfaces[2, ..., 0]**2 + surfaces[2, ..., 2]**2)**0.5
	a = np.arctan(surfaces[2, ..., 2] / (surfaces[2, ..., 0] + 1e-8))
	c = np.where(surfaces[2, ..., 0]>=0, 1, -1)
	a -= ang
	surfaces[2, ..., 0] = c*h*np.cos(a)
	surfaces[2, ..., 2] = c*h*np.sin(a)

def d_animate(ang):
	# rotates bottom face by the given angle
	h = (surfaces[[0, 1, 3, 4], :, 2, :, 0]**2 + surfaces[[0, 1, 3, 4], :, 2, :, 2]**2)**0.5
	a = np.arctan(surfaces[[0, 1, 3, 4], :, 2, :, 2] / (surfaces[[0, 1, 3, 4], :, 2, :, 0] + 1e-8))
	c = np.where(surfaces[[0, 1, 3, 4], :, 2, :, 0]>=0, 1, -1)
	a += ang
	surfaces[[0, 1, 3, 4], :, 2, :, 0] = c*h*np.cos(a)
	surfaces[[0, 1, 3, 4], :, 2, :, 2] = c*h*np.sin(a)

	h = (surfaces[5, ..., 0]**2 + surfaces[5, ..., 2]**2)**0.5
	a = np.arctan(surfaces[5, ..., 2] / (surfaces[5, ..., 0] + 1e-8))
	c = np.where(surfaces[5, ..., 0]>=0, 1, -1)
	a += ang
	surfaces[5, ..., 0] = c*h*np.cos(a)
	surfaces[5, ..., 2] = c*h*np.sin(a)

def l_animate(ang):
	x = np.array([surfaces[1, 0], surfaces[5, 2], surfaces[4, 2], surfaces[2, 0]])	# (4, 3, 4, 3)
	h = (x[..., 1]**2 + x[..., 2]**2)**0.5
	a = np.arctan(x[..., 2] / (x[..., 1] + 1e-8))
	c = np.where(x[..., 1]>=0, 1, -1)
	a += ang
	cos = c*h*np.cos(a)
	sin = c*h*np.sin(a)
	surfaces[1, 0, ..., 1], surfaces[5, 2, ..., 1], surfaces[4, 2, ..., 1], surfaces[2, 0, ..., 1] = cos
	surfaces[1, 0, ..., 2], surfaces[5, 2, ..., 2], surfaces[4, 2, ..., 2], surfaces[2, 0, ..., 2] = sin

	h = (surfaces[0, ..., 1]**2 + surfaces[0, ..., 2]**2)**0.5
	a = np.arctan(surfaces[0, ..., 2] / (surfaces[0, ..., 1] + 1e-8))
	c = np.where(surfaces[0, ..., 1]>=0, 1, -1)
	a += ang
	surfaces[0, ..., 1] = c*h*np.cos(a)
	surfaces[0, ..., 2] = c*h*np.sin(a)

def r_animate(ang):
	x = np.array([surfaces[1, 2], surfaces[5, 0], surfaces[4, 0], surfaces[2, 2]])	# (4, 3, 4, 3)
	h = (x[..., 1]**2 + x[..., 2]**2)**0.5
	a = np.arctan(x[..., 2] / (x[..., 1] + 1e-8))
	c = np.where(x[..., 1]>=0, 1, -1)
	a -= ang
	cos = c*h*np.cos(a)
	sin = c*h*np.sin(a)
	surfaces[1, 2, ..., 1], surfaces[5, 0, ..., 1], surfaces[4, 0, ..., 1], surfaces[2, 2, ..., 1] = cos
	surfaces[1, 2, ..., 2], surfaces[5, 0, ..., 2], surfaces[4, 0, ..., 2], surfaces[2, 2, ..., 2] = sin

	h = (surfaces[3, ..., 1]**2 + surfaces[3, ..., 2]**2)**0.5
	a = np.arctan(surfaces[3, ..., 2] / (surfaces[3, ..., 1] + 1e-8))
	c = np.where(surfaces[3, ..., 1]>=0, 1, -1)
	a -= ang
	surfaces[3, ..., 1] = c*h*np.cos(a)
	surfaces[3, ..., 2] = c*h*np.sin(a)

def f_animate(ang):
	h = (surfaces[1, ..., 0]**2 + surfaces[1, ..., 1]**2)**0.5
	a = np.arctan(surfaces[1, ..., 1] / (surfaces[1, ..., 0] + 1e-8))
	c = np.where(surfaces[1, ..., 2]>=0, 1, -1)
	a -= ang
	surfaces[1, ..., 1] = c*h*np.cos(a)
	surfaces[1, ..., 0] = c*h*np.sin(a)

def b_animate(ang):
	pass


"""
initial parameters:
0 -> left, red
1 -> front, green
2 -> top, yellow
3 -> right, orange
4 -> back, blue
5 -> bottom, white
"""

moves_animate = {0:u_animate, 1:d_animate, 2:l_animate, 3:r_animate, 4:f_animate, 5:b_animate}

def turn_face(face, angle):
	if face<6:
		moves_animate[face](angle)
	else:
		moves_animate[face-6](-angle)


# def u():
# 	# rotates top face clockwise
# 	h = (surfaces[[0, 1, 3, 4], :, 0, :, 0]**2 + surfaces[[0, 1, 3, 4], :, 0, :, 2]**2)**0.5
# 	a = np.arctan(surfaces[[0, 1, 3, 4], :, 0, :, 2] / (surfaces[[0, 1, 3, 4], :, 0, :, 0] + 1e-8))
# 	c = np.where(surfaces[[0, 1, 3, 4], :, 0, :, 0]>=0, 1, -1)
# 	a -= np.pi/2/30
# 	surfaces[[0, 1, 3, 4], :, 0, :, 0] = c*h*np.cos(a)
# 	surfaces[[0, 1, 3, 4], :, 0, :, 2] = c*h*np.sin(a)

# 	h = (surfaces[2, :, :, :, 0]**2 + surfaces[2, :, :, :, 2]**2)**0.5
# 	a = np.arctan(surfaces[2, :, :, :, 2] / (surfaces[2, :, :, :, 0] + 1e-8))
# 	c = np.where(surfaces[2, :, :, :, 0]>=0, 1, -1)
# 	a -= np.pi/2/30
# 	surfaces[2, :, :, :, 0] = c*h*np.cos(a)
# 	surfaces[2, :, :, :, 2] = c*h*np.sin(a)


# def d():
# 	# rotates bottom face clockwise
# 	h = (surfaces[[0, 1, 3, 4], :, 2, :, 0]**2 + surfaces[[0, 1, 3, 4], :, 2, :, 2]**2)**0.5
# 	a = np.arctan(surfaces[[0, 1, 3, 4], :, 2, :, 2] / (surfaces[[0, 1, 3, 4], :, 2, :, 0] + 1e-8))
# 	c = np.where(surfaces[[0, 1, 3, 4], :, 2, :, 0]>=0, 1, -1)
# 	a += np.pi/2/30
# 	surfaces[[0, 1, 3, 4], :, 2, :, 0] = c*h*np.cos(a)
# 	surfaces[[0, 1, 3, 4], :, 2, :, 2] = c*h*np.sin(a)

# 	h = (surfaces[5, :, :, :, 0]**2 + surfaces[5, :, :, :, 2]**2)**0.5
# 	a = np.arctan(surfaces[5, :, :, :, 2] / (surfaces[5, :, :, :, 0] + 1e-8))
# 	c = np.where(surfaces[5, :, :, :, 0]>=0, 1, -1)
# 	a += np.pi/2/30
# 	surfaces[5, :, :, :, 0] = c*h*np.cos(a)
# 	surfaces[5, :, :, :, 2] = c*h*np.sin(a)


# def l():
# 	x = np.array([surfaces[1, 0], surfaces[5, 2], surfaces[4, 2], surfaces[2, 0]])	# (4, 3, 4, 3)
# 	h = (x[..., 1]**2 + x[..., 2]**2)**0.5
# 	a = np.arctan(x[..., 2] / (x[..., 1] + 1e-8))
# 	c = np.where(x[..., 1]>=0, 1, -1)
# 	a -= np.pi/2/30
# 	cos = c*h*np.cos(a)
# 	sin = c*h*np.sin(a)
# 	surfaces[1, 0, ..., 1], surfaces[5, 2, ..., 1], surfaces[4, 2, ..., 1], surfaces[2, 0, ..., 1] = cos[0], cos[1], cos[2], cos[3]
# 	surfaces[1, 0, ..., 2], surfaces[5, 2, ..., 2], surfaces[4, 2, ..., 2], surfaces[2, 0, ..., 2] = sin[0], sin[1], sin[2], sin[3]

# 	h = (surfaces[0, ..., 1]**2 + surfaces[0, ..., 2]**2)**0.5
# 	a = np.arctan(surfaces[0, ..., 2] / (surfaces[0, ..., 1] + 1e-8))
# 	c = np.where(surfaces[0, ..., 1]>=0, 1, -1)
# 	a -= np.pi/2/30
# 	surfaces[0, ..., 1] = c*h*np.cos(a)
# 	surfaces[0, ..., 2] = c*h*np.sin(a)


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
	# if v==13:
	# 	t = font.render("Front", True, (0,0,0))
	# 	win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))
	# if v==22:
	# 	t = font.render("Up", True, (0,0,0))
	# 	win.blit(t, np.mean(s, axis=0)-np.array([t.get_width()/2, t.get_height()/2]))
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
	for i, s in enumerate(string):
		t = font.render(s, True, clrs[5])
		win.blit(t, (10, 10+i*25))
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


alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01
inc = 0.02
fps = 0
# up_timer = down_timer = left_timer = right_timer = front_timer = back_timer = 0
# up_timer_ = down_timer_ = left_timer_ = right_timer_ = front_timer_ = back_timer_ = 0
# key_press = np.zeros(12, dtype=bool)
timer = 0
turn_speed = 30
# up = down = left = right = front = back = False
# up_ = down_ = left_ = right_ = front_ = back_ = False
wait = 150
interval = 0
p_interval = 0
run = True


print("Rotate cube: Arrow Keys\nShuffle: SHIFT + S\nSolve: CTRL + S\nMoves (clockwise): F B R L D B\nMoves (anti-clockwise): SHIFT + (F B R L D B)")
string = ["Rotate cube: Arrow Keys", "Shuffle: SHIFT + S", "Solve: CTRL + S", "Moves (clockwise): F B R L D B", "Moves (anti-clockwise): SHIFT + (F B R L D B)"]

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

	if keyp[pg.K_u] and timer==0:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			n = 6
		else:
			n = 0
		timer = 1
	if keyp[pg.K_d] and timer==0:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			n = 7
		else:
			n = 1
		timer = 1
	if keyp[pg.K_l] and timer==0:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			n = 8
		else:
			n = 2
		timer = 1
	if keyp[pg.K_r] and timer==0:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			n = 9
		else:
			n = 3
		timer = 1
	if keyp[pg.K_f] and timer==0:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			n = 10
		else:
			n = 4
		timer = 1
	if keyp[pg.K_b] and timer==0:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			n = 11
		else:
			n = 5
		timer = 1


	if keyp[pg.K_s] and keyp[pg.K_LSHIFT]:
		shuffle()
		pg.time.delay(wait)

	if keyp[pg.K_LCTRL]:
		if keyp[pg.K_s]:
			solve()
			alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01
		elif keyp[pg.K_z]:
			undo()

	fps = pf()

	if timer>0:
		turn_face(n, np.pi/turn_speed/2)
		timer += 1
		if timer == turn_speed+1:
			timer = 0
			turn_face(n, -np.pi/2)
			taken.append(n)
			moves[n]()


	if alpha > 2*np.pi or alpha < -2*np.pi:
		alpha = 0
	if beta > np.pi/2:
		beta = np.pi/2 + 0.01
	if beta < -np.pi/2:
		beta = -np.pi/2 + 0.01

	# interval = int(2*(alpha+(1 if alpha>0 else -1)*np.pi/4)/np.pi)%4
	# if interval>p_interval:
	# 	change_front(0)
	# 	taken.append(12)
	
	draw()

	# if pf()%1 < 0.01:
	# 	print(f"FPS: {round(1/(pf()-fps))}")



"""
# U
if up and up_timer<30:
	up_timer += 1
	u()
else:
	up = False
	if up_timer>0:
		surfaces[[0, 1, 3, 4], :, 0] = surfaces[[1, 3, 4, 0], :, 0]
		colors[[0,3,6,9,12,15,27,30,33,36,39,42]] = colors[[9,12,15,27,30,33,36,39,42,0,3,6]]
	up_timer = 0

# D
if down and down_timer<30:
	down_timer += 1
	d()
else:
	down = False
	if down_timer>0:
		surfaces[[0, 1, 3, 4], :, 2] = surfaces[[4, 0, 1, 3], :, 2]
		colors[[2,5,8,11,14,17,29,32,35,38,41,44]] = colors[[38,41,44,2,5,8,11,14,17,29,32,35]]
	down_timer = 0

# L
if left and left_timer<30:
	left_timer += 1
	l()
else:
	left = False
	if left_timer>0:
		# 
		surfaces[[0, 1, 3, 4], :, 2] = surfaces[[4, 0, 1, 3], :, 2]
		colors[[2,5,8,11,14,17,29,32,35,38,41,44]] = colors[[38,41,44,2,5,8,11,14,17,29,32,35]]
	left_timer = 0
"""


""" 
to add:
	undo
	redo
	animations
	AI to solve
"""
