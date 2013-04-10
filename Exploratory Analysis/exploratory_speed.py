import json
import numpy as np
import matplotlib.pyplot as plt
users = []

def get_duration(workout):
	duration = 0
	try:
		duration = workout['activity']['duration']
	except:
		duration = 0
	if duration == 0:
		try: 
			for item in workout['activity']['history']:
				if item['type'] == "SPEED" and item['intervalUnit'] == "SEC":
					duration = len(item['values']) * item['intervalMetric'] * 1000
		except:
			duration = 0
	return duration
	
def get_distance(workout):
	return workout['activity']['distance']

def get_average(dur_dist_list):
	speeds = []
	for item in dur_dist_list:
		speeds.append(float(item['distance'])/float(item['duration']))
	average = sum(speeds) / len(speeds) * 60
	return average
	
def get_average_dist(dur_dist_list):
	dist = []
	for item in dur_dist_list:
		dist.append(float(item['distance']))
	average = sum(dist) / len(dist)
	return average

IN_FILE = open("crappy_workout_json.txt", "r")
for user in IN_FILE:
	try:
		loc_user = []
		data = json.loads(user)
		for workout in data['workouts']:
			try:
				duration = get_duration(workout)
				distance = get_distance(workout)
				if duration != 0 and distance != 0:
					#the 60k is to go from ms to minutes
					#also the .621371192 is to go from km to miles. 
					loc_user.append({'duration':float(duration)/60000, 'distance':float(distance)*0.621371192})
			except:
				continue
		if len(loc_user) > 0:
			users.append({'user_id':data['user_id'], 'dur_dist_list':loc_user})
	except:
		continue
speed = []
for item in users:
	average = get_average(item['dur_dist_list'])
	speed.append(average)
new_speed = [(item/60)**-1 for item in speed]

buckets = [.5*x for x in range(0,26)]
#hist, bin_edges = np.histogram(speed, bins = buckets)
hist, bin_edges = np.histogram(new_speed, bins = buckets)
print hist


plt.figure()		
#plt.hist(speed, bins=buckets)
plt.hist(new_speed, bins=buckets)
plt.title("Average Min/Mile for Individuals")


distances = []
for item in users:
	average = get_average_dist(item['dur_dist_list'])
	distances.append(average)
hist, bin_edges = np.histogram(distances, bins = buckets)
print hist

plt.figure()
plt.hist(distances, bins = buckets)
plt.title("Average Dist in Miles for Individuals")
plt.show()



	
		