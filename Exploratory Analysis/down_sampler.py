import numpy as np
import matplotlib.pyplot as plt
from utils import *

if __name__ == "__main__":
	file = open("distance.txt")

	speed_a = np.array([float(elem) for elem in file.readline()[1:-2].split(',')])
	speed_b = np.array([float(elem) for elem in file.readline()[1:-2].split(',')])
	speed_c = np.array([float(elem) for elem in file.readline()[1:-2].split(',')])

	#speed_a = np.sin(.1*np.pi*np.arange(200))
	#speed_b = np.sin(.1*np.pi*np.arange(200))+.1
	#speed_c = np.sin(.1*np.pi*np.arange(200))+.3


	down_a = down_sample(speed_a, 100)
	down_b = down_sample(speed_b, 100)
	down_c = down_sample(speed_c, 100)

	down_a /= max(down_a)	
	down_b /= max(down_b)
	down_c /= max(down_c)

	print temporal_similarity(down_a ,down_b)
	plt.figure()
	plt.plot(speed_a)
	plt.plot(speed_b,'r')
	plt.plot(speed_c,'g')
	plt.figure()
	plt.plot(down_a)
	plt.plot(down_b,'r')
	plt.plot(down_c,'g')
	plt.show()

