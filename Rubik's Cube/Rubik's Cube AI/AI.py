import numpy as np
from Cube_functions import *

"white -> 45 to 53"

side_face_list = [[0, 9], [9, 18], [27, 36], [36, 45]]


def algorithm(algo, moves_to_take, cube):
	lis = algo.split(' ')
	for l in lis:
		if l[0]=='2':
			for _ in range(2):
				x = algo_move[l[1:]]
				moves_to_take.append(x)
				moves[x](cube)
		elif len(l) > 1 and l[1]=='2':
			for _ in range(2):
				x = algo_move[l[0]]
				moves_to_take.append(x)
				moves[x](cube)

		else:
			x = algo_move[l]
			moves_to_take.append(x)
			moves[x](cube)



def cross(colors):
	s_cube = np.copy(colors)

	moves_to_take = []

	while not np.all(s_cube[19:26:2]==255):
		# identifying white edge piece
		idx = -1
		for i, c in enumerate(np.concatenate((s_cube[:18], s_cube[27:]))):
			if (i%9)%2==1 and np.all(c==255):
				idx = i if i<18 else i+9
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
				while np.all(s_cube[19]==255):
					fu(s_cube)
					moves_to_take.append(0)
				fl_(s_cube)
				moves_to_take.append(8)
			elif fidx==16:
				while np.all(s_cube[25]==255):
					fu(s_cube)
					moves_to_take.append(0)
				fr(s_cube)
				moves_to_take.append(3)
			elif fidx==12:
				while np.all(s_cube[23]==255):
					fu(s_cube)
					moves_to_take.append(0)
				ff(s_cube)
				fu_(s_cube)
				fr(s_cube)
				moves_to_take.append(4)
				moves_to_take.append(6)
				moves_to_take.append(3)
			elif fidx==14:
				while np.all(s_cube[23]==255):
					fu(s_cube)
					moves_to_take.append(0)
				ff_(s_cube)
				fu_(s_cube)
				fr(s_cube)
				moves_to_take.append(10)
				moves_to_take.append(6)
				moves_to_take.append(3)

		# if white edge piece is on the bottom face
		else:
			if idx==50:
				while np.all(s_cube[23]==255):
					fu(s_cube)
					moves_to_take.append(0)
				ff(s_cube)
				ff(s_cube)
				moves_to_take.append(4)
				moves_to_take.append(4)
			elif idx==46:
				while np.all(s_cube[25]==255):
					fu(s_cube)
					moves_to_take.append(0)
				fr(s_cube)
				fr(s_cube)
				moves_to_take.append(3)
				moves_to_take.append(3)
			elif idx==48:
				while np.all(s_cube[21]==255):
					fu(s_cube)
					moves_to_take.append(0)
				fb(s_cube)
				fb(s_cube)
				moves_to_take.append(5)
				moves_to_take.append(5)
			elif idx==52:
				while np.all(s_cube[19]==255):
					fu(s_cube)
					moves_to_take.append(0)
				fl(s_cube)
				fl(s_cube)
				moves_to_take.append(2)
				moves_to_take.append(2)

	return moves_to_take


def align_cross(colors):
	moves_to_take = []

	s_cube = np.copy(colors)

	for _ in range(4):
		while not (np.all(s_cube[12]==s_cube[13]) and np.all(s_cube[23]==255)):
			algorithm("U", moves_to_take, s_cube)

		algorithm("2F", moves_to_take, s_cube)

		change_front(0, s_cube)
		moves_to_take.append(12)

	return moves_to_take


def corners(colors):
	moves_to_take = []
	cube = np.copy(colors)
	# checking the colors of the corners

	def check():
		for i in [4, 13, 31, 40]:
			if not (np.all(cube[i]==cube[i-2]) and np.all(cube[i]==cube[i+4])):
				return False
		return True

	# checking if corners are put correctly
	while not (np.all(cube[[53, 47, 51, 45]]==255) and check()):
		# finding the white corner piece
		for i in range(54):
			if (i%9)%2==0 and np.all(cube[i]==255) and i!=49:
				idx = i
				break

		# if idx is in side faces
		if (idx>=0 and idx<18) or (idx>=27 and idx<45):
			# identifying which face to switch to
			for f, l in enumerate(side_face_list):
				if idx>=l[0] and idx<l[1]:
					face = f
					break

			if face==0:
				change_front(0, cube)
				moves_to_take.append(12)
			elif face==2:
				change_front(1, cube)
				moves_to_take.append(13)
			elif face==3:
				change_front(0, cube)
				moves_to_take.append(12)
				change_front(0, cube)
				moves_to_take.append(12)

			# switched to the correct face
			fidx = idx%9 + 9
			# checking which corner it is out of 4 possible cases
			if fidx==9:		# top left
				while not np.all(cube[[6, 20]]==cube[[40, 4]]):
					algorithm("U", moves_to_take, cube)
					change_front(0, cube)
					moves_to_take.append(12)
				algorithm("B' U B", moves_to_take, cube)
			elif fidx==15:	# top right
				while not np.all(cube[[26, 27]]==cube[[31, 40]]):
					algorithm("U'", moves_to_take, cube)
					change_front(1, cube)
					moves_to_take.append(13)
				algorithm("B U' B'", moves_to_take, cube)
			elif fidx==11:	# bottom left
				# taking out the corner
				algorithm("L' U L", moves_to_take, cube)
				# same as top left
				while not np.all(cube[[6, 20]]==cube[[40, 4]]):
					algorithm("U", moves_to_take, cube)
					change_front(0, cube)
					moves_to_take.append(12)
				algorithm("B' U B", moves_to_take, cube)
			elif fidx==17:	# bottom right
				# taking out the corner
				algorithm("R U' R'", moves_to_take, cube)
				# same as top right
				while not np.all(cube[[26, 27]]==cube[[31, 40]]):
					algorithm("U'", moves_to_take, cube)
					change_front(1, cube)
					moves_to_take.append(13)
				algorithm("B U' B'", moves_to_take, cube)

		# if idx is in the top face
		elif idx>=18 and idx<27:
			# place the front such that corner is at bottom right wrt front
			while not np.all(cube[26]==255):
				change_front(0, cube)
				moves_to_take.append(12)
			# putting over the correct position
			while not np.all(cube[[15, 27]]==cube[[31, 13]]):
				algorithm("U", moves_to_take, cube)
				change_front(0, cube)
				moves_to_take.append(12)
			# putting at the correct position
			algorithm("R U' R' U F' U F", moves_to_take, cube)

		# if idx is in the bottom face
		elif idx>=45 and idx<54:
			# change front such that white corner is in front right
			while not np.all(cube[47]==255):
				change_front(1, cube)
				moves_to_take.append(13)
			algorithm("F' U F", moves_to_take, cube)
			# now same as top right case of side face
			while not np.all(cube[[26, 27]]==cube[[13, 31]]):
				fu_(cube)
				change_front(1, cube)
				moves_to_take.append(6)
				moves_to_take.append(13)
			algorithm("U R U' R'", moves_to_take, cube)

	return moves_to_take


def edges(colors):
	moves_to_take = []
	cube = np.copy(colors)

	top_edge_list = np.array([[3, 19], [23, 12], [30, 25], [39, 21]])
	se_list = np.array([[7, 10], [16, 28], [34, 37], [43, 1]])
	ec_list = np.array([[4, 13], [13, 31], [31, 40], [40, 4]])

	while np.any(cube[ec_list.flatten()] != cube[se_list.flatten()]):
		# checking for edges in the top layer
		face = -1
		for i, l in enumerate(top_edge_list):
			if not np.any(cube[l, 1] == 238):
				face = i
				break

		if face >= 0:
			# changing face according to edge
			if face==0:
				change_front(0, cube)
				moves_to_take.append(12)
			elif face==1:
				pass
			elif face==2:
				change_front(1, cube)
				moves_to_take.append(13)
			elif face==3:
				for _ in range(2):
					change_front(1, cube)
					moves_to_take.append(13)
			else:
				pass

			# aligning with matching centre
			if np.all(cube[12]==cube[13]):
				pass
			elif np.all(cube[12]==cube[4]):
				change_front(0, cube)
				moves_to_take.append(12)
				algorithm("U", moves_to_take, cube)
			elif np.all(cube[12]==cube[31]):
				change_front(1, cube)
				moves_to_take.append(13)
				algorithm("U'", moves_to_take, cube)
			else:
				for _ in range(2):
					change_front(1, cube)
					moves_to_take.append(13)
				algorithm("2U", moves_to_take, cube)

			# finding correct place for edge (left or right)
			if np.all(cube[23]==cube[31]):		# right
				algorithm("U R U' R' U' F' U F", moves_to_take, cube)
			else:		# left -> np.all(cube[4]==cube[23])
				algorithm("U' L' U L U F U' F'", moves_to_take, cube)

		# taking out incorrectly placed edge
		else:
			face = -1
			# finding the edge
			for i, e in enumerate(se_list):
				if np.any(cube[e]!=cube[ec_list[i]]):
					face = i
			# the edge should be at left position of front face, so changing face
			if face==1:
				change_front(1, cube)
				moves_to_take.append(13)
				algorithm("U'", moves_to_take, cube)
			elif face==2:
				for _ in range(2):
					change_front(1, cube)
					moves_to_take.append(13)
				algorithm("2U", moves_to_take, cube)
			elif face==3:
				change_front(0, cube)
				moves_to_take.append(12)
				algorithm("U", moves_to_take, cube)

			# taking out the edge
			algorithm("U' L' U L U F U' F'", moves_to_take, cube)

	return moves_to_take

