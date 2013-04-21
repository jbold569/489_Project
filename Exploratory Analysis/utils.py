import json

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