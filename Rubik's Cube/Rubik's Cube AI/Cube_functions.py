import numpy as np

# animations
def u_animate(ang, surfaces):
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

def d_animate(ang, surfaces):
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

def l_animate(ang, surfaces):
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

def r_animate(ang, surfaces):
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

def f_animate(ang, surfaces):
	x = np.array([surfaces[0, 2], surfaces[2, :, 2], surfaces[3, 0], surfaces[5, :, 2]])
	h = (x[..., 0]**2 + x[..., 1]**2)**0.5
	a = np.arctan(x[..., 1] / (x[..., 0] + 1e-8))
	c = np.where(x[..., 0]>=0, 1, -1)
	a += ang
	cos = c*h*np.cos(a)
	sin = c*h*np.sin(a)
	surfaces[0, 2, ..., 0], surfaces[2, :, 2, ..., 0], surfaces[3, 0, ..., 0], surfaces[5, :, 2, ..., 0] = cos
	surfaces[0, 2, ..., 1], surfaces[2, :, 2, ..., 1], surfaces[3, 0, ..., 1], surfaces[5, :, 2, ..., 1] = sin
	
	h = (surfaces[1, ..., 0]**2 + surfaces[1, ..., 1]**2)**0.5
	a = np.arctan(surfaces[1, ..., 1] / (surfaces[1, ..., 0] + 1e-8))
	c = np.where(surfaces[1, ..., 0]>=0, 1, -1)
	a += ang
	surfaces[1, ..., 0] = c*h*np.cos(a)
	surfaces[1, ..., 1] = c*h*np.sin(a)

def b_animate(ang, surfaces):
	x = np.array([surfaces[0, 0], surfaces[2, :, 0], surfaces[3, 2], surfaces[5, :, 0]])
	h = (x[..., 0]**2 + x[..., 1]**2)**0.5
	a = np.arctan(x[..., 1] / (x[..., 0] + 1e-8))
	c = np.where(x[..., 0]>=0, 1, -1)
	a -= ang
	cos = c*h*np.cos(a)
	sin = c*h*np.sin(a)
	surfaces[0, 0, ..., 0], surfaces[2, :, 0, ..., 0], surfaces[3, 2, ..., 0], surfaces[5, :, 0, ..., 0] = cos
	surfaces[0, 0, ..., 1], surfaces[2, :, 0, ..., 1], surfaces[3, 2, ..., 1], surfaces[5, :, 0, ..., 1] = sin
	
	h = (surfaces[4, ..., 0]**2 + surfaces[4, ..., 1]**2)**0.5
	a = np.arctan(surfaces[4, ..., 1] / (surfaces[4, ..., 0] + 1e-8))
	c = np.where(surfaces[4, ..., 0]>=0, 1, -1)
	a -= ang
	surfaces[4, ..., 0] = c*h*np.cos(a)
	surfaces[4, ..., 1] = c*h*np.sin(a)

# cube functions (moves)
# f (before every move name) means fast lol
def fu(colors):
	colors[[0,3,6,9,12,15,27,30,33,36,39,42]] = colors[[9,12,15,27,30,33,36,39,42,0,3,6]]
	colors[[18,19,20,23,26,25,24,21]] = colors[[20,23,26,25,24,21,18,19]]
	# print("U", end=' ')

def fu_(colors):
	colors[[0,3,6,9,12,15,27,30,33,36,39,42]] = colors[[36,39,42,0,3,6,9,12,15,27,30,33]]
	colors[[18,19,20,23,26,25,24,21]] = colors[[24,21,18,19,20,23,26,25]]
	# print("U'", end=' ')

def fd(colors):
	colors[[2,5,8,11,14,17,29,32,35,38,41,44]] = colors[[38,41,44,2,5,8,11,14,17,29,32,35]]
	colors[[53,50,47,46,45,48,51,52]] = colors[[51,52,53,50,47,46,45,48]]
	# print("D", end=' ')

def fd_(colors):
	colors[[2,5,8,11,14,17,29,32,35,38,41,44]] = colors[[11,14,17,29,32,35,38,41,44,2,5,8]]
	colors[[53,50,47,46,45,48,51,52]] = colors[[47,46,45,48,51,52,53,50]]
	# print("D'", end=' ')

def fl(colors):
	colors[[18,19,20,9,10,11,53,52,51,44,43,42]] = colors[[44,43,42,18,19,20,9,10,11,53,52,51]]
	colors[[0,1,2,5,8,7,6,3]] = colors[[2,5,8,7,6,3,0,1]]
	# print("L", end=' ')

def fl_(colors):
	colors[[18,19,20,9,10,11,53,52,51,44,43,42]] = colors[[9,10,11,53,52,51,44,43,42,18,19,20]]
	colors[[0,1,2,5,8,7,6,3]] = colors[[6,3,0,1,2,5,8,7]]
	# print("L'", end=' ')

def fr(colors):
	colors[[24,25,26,15,16,17,47,46,45,38,37,36]] = colors[[15,16,17,47,46,45,38,37,36,24,25,26]]
	colors[[27,28,29,32,35,34,33,30]] = colors[[29,32,35,34,33,30,27,28]]
	# print("R", end=' ')

def fr_(colors):
	colors[[24,25,26,15,16,17,47,46,45,38,37,36]] = colors[[38,37,36,24,25,26,15,16,17,47,46,45]]
	colors[[27,28,29,32,35,34,33,30]] = colors[[33,30,27,28,29,32,35,34]]
	# print("R'", end=' ')

def ff(colors):
	colors[[6,7,8,53,50,47,29,28,27,26,23,20]] = colors[[53,50,47,29,28,27,26,23,20,6,7,8]]
	colors[[9,10,11,14,17,16,15,12]] = colors[[11,14,17,16,15,12,9,10]]
	# print("F", end=' ')

def ff_(colors):
	colors[[6,7,8,53,50,47,29,28,27,26,23,20]] = colors[[26,23,20,6,7,8,53,50,47,29,28,27]]
	colors[[9,10,11,14,17,16,15,12]] = colors[[15,12,9,10,11,14,17,16]]
	# print("F'", end=' ')

def fb(colors):
	colors[[0,1,2,51,48,45,35,34,33,24,21,18]] = colors[[24,21,18,0,1,2,51,48,45,35,34,33]]
	colors[[36,37,38,41,44,43,42,39]] = colors[[38,41,44,43,42,39,36,37]]
	# print("B", end=' ')

def fb_(colors):
	colors[[0,1,2,51,48,45,35,34,33,24,21,18]] = colors[[51,48,45,35,34,33,24,21,18,0,1,2]]
	colors[[36,37,38,41,44,43,42,39]] = colors[[42,39,36,37,38,41,44,43]]
	# print("B'", end=' ')


def turn_face(face, angle, surfaces):
	if face<6:
		moves_animate[face](angle, surfaces)
	else:
		moves_animate[face-6](-angle, surfaces)


lists = [[i for i in range(9)], [i for i in range(9, 18)], [i for i in range(27, 36)], [i for i in range(36, 45)]]

# for changing the front face when cube is rotated
def change_front(face, colors):
	if face==0:
		colors[lists[0]+lists[1]+lists[2]+lists[3]] = colors[lists[3]+lists[0]+lists[1]+lists[2]]
		colors[[18,19,20,23,26,25,24,21]] = colors[[24,21,18,19,20,23,26,25]]
		colors[[53,50,47,46,45,48,51,52]] = colors[[51,52,53,50,47,46,45,48]]
	else:
		colors[lists[0]+lists[1]+lists[2]+lists[3]] = colors[lists[1]+lists[2]+lists[3]+lists[0]]
		colors[[18,19,20,23,26,25,24,21]] = colors[[20,23,26,25,24,21,18,19]]
		colors[[53,50,47,46,45,48,51,52]] = colors[[47,46,45,48,51,52,53,50]]

moves_animate = {0:u_animate, 1:d_animate, 2:l_animate, 3:r_animate, 4:f_animate, 5:b_animate}
moves = {0:fu, 1:fd, 2:fl, 3:fr, 4:ff, 5:fb, 6:fu_, 7:fd_, 8:fl_, 9:fr_, 10:ff_, 11:fb_, 12:change_front}

