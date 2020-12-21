import numpy as np
from Cube_functions import *

"white -> 45 to 53"

side_face_list = [[0, 9], [9, 18], [27, 36], [36, 45]]


def check_cross(colors):
	if np.mean(colors[46:53:2] == [255, 255, 255]) == 1:
		return True

