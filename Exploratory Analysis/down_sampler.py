import numpy as np
import matplotlib.pyplot as plt

def down_sample(data, size):
	size = 100
	extra = len(data)%size
	down = []
	num_samples = len(data)/size
	
	# This loop averages num_samples plus 1 for the number samples over 
	# Example: 456 samples down sampled by do 100 will  have 56 samples over
	# to fix this the first 56 down samples will be an average of 5 sample instead of 4
	for i in range(extra):
		offset = i*(num_samples+1)
		average = sum(data[offset : offset+num_samples+1])/float(num_samples+1)
		down.append(average)
	
	# Continues down sampling with the correct number of samples per down sample
	for i in range(extra, size):
		offset = (i-extra)*num_samples+extra*(num_samples+1)
		average = sum(data[offset : offset+num_samples])/float(num_samples)
		down.append(average)
	
	return down


file = open("distance.txt")

speed = np.array([float(elem) for elem in file.readline()[1:-2].split(',')])
distance = np.array([float(elem) for elem in file.readline()[1:-2].split(',')])

down_sampled_speed = down_sample(speed, 100)
	
down_sampled_speed /= max(down_sampled_speed)

plt.figure()
plt.plot(speed)
plt.figure()
plt.plot(down_sampled_speed)
plt.show()

