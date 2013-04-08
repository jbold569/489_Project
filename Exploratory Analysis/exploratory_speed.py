import json
import numpy as np
users = []

def get_average(dur_dist_list):
	speeds = []
	for item in dur_dist_list:
		speeds.append(float(item['distance'])/float(item['duration']))
	average = sum(speeds) / len(speeds) * 60
	return average

IN_FILE = open("crappy_workout_json.txt", "r")
for user in IN_FILE:
	try:
		loc_user = []
		data = json.loads(user)
		for workout in data['workouts']:
			try:
				duration = workout['activity']['duration']
				distance = workout['activity']['distance']
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
buckets = [.5*x for x in range(0,26)]
hist, bin_edges = np.histogram(speed, bins = buckets)
print hist

	
		