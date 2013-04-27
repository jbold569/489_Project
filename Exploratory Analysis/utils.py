import json
import numpy as np

def down_sample(data, size):
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
	
	return np.array(down)
	
def temporal_similarity(Tp, Tq):
	sum = 0.0
	u_Tp = np.mean(Tp)
	u_Tq = np.mean(Tq)
	s_Tp = np.std(Tp)
	s_Tq = np.std(Tq)
	
	for i in range(len(Tp)):
		left = (Tp[i]-u_Tp)/s_Tp
		right = (Tq[i]-u_Tq)/s_Tq
		sum += left*right
		
	return sum/len(Tp)
	
def cosine_simularity(V,U):
	sum_V = 0.0
	sum_U = 0.0
	sum_product = 0.0
	for v,u in zip(V,U):
		sum_V += v**2
		sum_U += u**2
		sum_product += v*u
	mag_V = sum_V/len(V)
	mag_U = sum_U/len(U)
	return 1 - sum_product/(mag_V*mag_U)
	
def euclidean_simularity(V,U):
	sum = 0.0
	for v,u in zip(V,U):
		sum += (v-u)**2
	return sum**0.5

# Returns a list of centroids
def canopy_clustering(t1, t2, data, sim_func = None):
	# t1>t2
	from random import shuffle
	from collections import defaultdict
	
	dCanopies = defaultdict(list)
	n = 0
	original_list = data
	shuffle(original_list)
	print "What? ", original_list
	while original_list:
		vec = original_list[0]
		canopy = [elem for elem in original_list if t1 > sim_func(vec,elem)]
		original_list = [elem for elem in original_list if not t2 > sim_func(vec, elem)]
		dCanopies[n] = canopy
		n+=1
	print dCanopies
	centers = []
	for points in dCanopies.values():
		total = sum(np.array(points))
		centers.append(total/float(len(points)))
	
	return np.array(centers)
		
def incStat(stat, data, key):
	if sGet(data, key):
		stat[sGet(data, key)] += 1
	else:
		stat['NA'] += 1

def appendStat(stat, data, key):
	if sGet(data, key):
		stat.append(sGet(data, key))
		return True
	else:
		return False

def sLoad(line):
	try:
		return json.loads(line)
	except ValueError as e:
		#print e
		return None
		
def sGet(data, key):
	try:
		return data[key]
	except KeyError as e:
		#print e
		return None
	except TypeError as e:
		return None