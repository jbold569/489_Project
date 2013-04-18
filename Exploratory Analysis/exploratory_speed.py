import json
import numpy as np
import matplotlib.pyplot as plt
users = []
num_workouts = 0
num_usable = 0

def get_start_time(workout):
	try:
		return workout['activity']['startTimeUtc']
	except:
		return None

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
	try:
		return workout['activity']['distance']
	except:
		return 0
def get_fuel(workout):
	try:
		return workout['activity']['fuel']
	except:
		return 0


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
	
def get_average_fuel(dur_dist_list):
	fuel = []
	for item in dur_dist_list:
		fuel.append(float(item['fuel']))
	return sum(fuel)/len(fuel)

IN_FILE = open("crappy_workout_json.txt", "r")
for user in IN_FILE:
	try:
		loc_user = []
		data = json.loads(user)
		num_workouts += len(data['workouts'])
		for workout in data['workouts']:
			if workout:
				num_usable+=1
			try:
				duration = get_duration(workout)
				distance = get_distance(workout)
				start_time = get_start_time(workout)
				#print start_time
				fuel = get_fuel(workout)
				if duration != 0 and distance != 0:
					#the 60k is to go from ms to minutes
					#also the .621371192 is to go from km to miles. 
					loc_user.append({'duration':float(duration)/60000, 'distance':float(distance)*0.621371192, 'fuel':float(fuel)})
			except:
				continue
		if len(loc_user) > 0:
			users.append({'user_id':data['user_id'], 'dur_dist_list':loc_user})
	except:
		continue
speed = []
distances = []
corr = []
fuels = []
fuel_buckets = [50*x for x in range(0,30)]
buckets = [.5*x for x in range(0,26)]
for item in users:
	saverage = get_average(item['dur_dist_list'])
	speed.append(saverage)
	
	daverage = get_average_dist(item['dur_dist_list'])
	distances.append(daverage)
	
	faverage = get_average_fuel(item['dur_dist_list'])
	fuels.append(faverage)
new_speed = [(item/60)**-1 for item in speed]

from math import floor

for sp, dist in zip(new_speed, distances):
	try:
		s = buckets[int(floor(sp/0.5))]
		d = buckets[int(floor(dist/0.5))]
		corr.append(('['+str(s)+' '+str(s+0.5)+')', '['+str(d)+' '+str(d+0.5)+')'))
	except:
		pass
file = open('corr.csv', 'w')
for c in corr:
	file.write(str(c)[1:-1]+'\n')
file.close()

print "buckets", buckets

#hist, bin_edges = np.histogram(speed, bins = buckets)
hist, bin_edges = np.histogram(new_speed, bins = buckets)
f_speed = open("speed.txt", 'w')
for item in new_speed:
	f_speed.write(str(item) + '\n')
f_speed.close()
	

plt.figure()		
#plt.hist(speed, bins=buckets)
plt.hist(new_speed, bins=buckets)
plt.title("Average Min/Mile for Individuals")
	
hist, bin_edges = np.histogram(distances, bins = buckets)
f_dist = open("dist.txt", 'w')
for item in distances:
	f_dist.write(str(item) + '\n')
f_dist.close()

plt.figure()
plt.hist(distances, bins = buckets)
plt.title("Average Dist in Miles for Individuals")

#print "Num workouts", num_workouts
#print "Num usable", num_usable

plt.figure()
plt.hist(fuels, bins = fuel_buckets)
plt.title("Average Fuel for Individuals")
plt.show()

	
		