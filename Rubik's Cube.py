import pygame as pg
import numpy as np
from time import perf_counter as pf


print("\n\nMoves : F, B, R, L, U, D, SHIFT + F, SHIFT + B, SHIFT + R, SHIFT + L, SHIFT + U, SHIFT + D\nShuffle : SHIFT + S\nSolve : CTRL + S\nChange Cube Angle : Arrow keys (UP, DOWN, LEFT, RIGHT)\n")



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


clrs = {0:(255, 0, 0), 1:(0, 255, 0), 2:(255, 255, 0), 3:(255, 135, 0), 4:(0, 0, 255), 5:(255, 255, 255)}
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

"""
0 -> left, red
1 -> front, green
2 -> top, yellow
3 -> right, orange
4 -> back, blue
5 -> bottom, white
"""

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

# takes random moves
def shuffle():
	print()
	for i in range(30):
		x = np.random.randint(0, 12)
		moves[x]()
		taken.append(x)
		draw()


# reverses the taken moves
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
		pg.draw.line(win, (32, 32, 32), s[i], s[i+1])
	pg.draw.line(win, (32, 32, 32), s[0], s[3])
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

	# arranging faces according to their distance from the viewer
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

	k = (L/(L + cube[..., 2]*t)).reshape(6, 3, 3, 4, 1)		# perspective scaling factor
	z = np.mean(cube[..., 2], axis=3).reshape(54)
	
	return W//2 + (k*cube[..., :2]).reshape(54, 4, 2), z


alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01
inc = 0.02
fps = 0
timer = 0
up = down = left = right = front = back = False
wait = 150
interval = 0
p_interval = 0


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

	if keyp[pg.K_u]:
		up = True
	if keyp[pg.K_d]:
		down = True
	if keyp[pg.K_l]:
		left = True
	if keyp[pg.K_r]:
		right = True
	if keyp[pg.K_f]:
		front = True
	if keyp[pg.K_b]:
		back = True

	if keyp[pg.K_s] and keyp[pg.K_LSHIFT]:
		shuffle()
		pg.time.delay(wait)

	if keyp[pg.K_s] and keyp[pg.K_LCTRL]:
		solve()
		alpha, beta = np.pi/4 + 0.01, -np.pi/4 + 0.01

	fps = pf()

	if up:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			fu_()
			taken.append(6)
		else:
			fu()
			taken.append(0)
		up = False
		pg.time.delay(wait)

	if down:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			fd_()
			taken.append(7)
		else:
			fd()
			taken.append(1)
		down = False
		pg.time.delay(wait)

	if left:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			fl_()
			taken.append(8)
		else:
			fl()
			taken.append(2)
		left = False
		pg.time.delay(wait)

	if right:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			fr_()
			taken.append(9)
		else:
			fr()
			taken.append(3)
		right = False
		pg.time.delay(wait)

	if front:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			ff_()
			taken.append(10)
		else:
			ff()
			taken.append(4)
		front = False
		pg.time.delay(wait)

	if back:
		if keyp[pg.K_LSHIFT] or keyp[pg.K_RSHIFT]:
			fb_()
			taken.append(11)
		else:
			fb()
			taken.append(5)
		back = False
		pg.time.delay(wait)


	if alpha > 2*np.pi or alpha < -2*np.pi:
		alpha = 0
	if beta > np.pi/2:
		beta = np.pi/2 + 0.01
	if beta < -np.pi/2:
		beta = -np.pi/2 + 0.01

	interval = int(2*(alpha+(1 if alpha>0 else -1)*np.pi/4)/np.pi)%4
	if interval>p_interval:
		change_front(0)
		taken.append(12)
	
	draw()

	# if pf()%1 < 0.01:
	# 	print(f"FPS: {round(1/(pf()-fps))}")

