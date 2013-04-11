import json

num_dist = 0
num_dur = 0
num_weather = 0
num_terrain = 0
num_gps = 0
fuel = 0
calories = 0
emotion = 0

def get_duration(workout):
	duration = 0
	try:
		duration = workout['activity']['duration']
		return 1
	except:
		duration = 0
	if duration == 0:
		try: 
			for item in workout['activity']['history']:
				if item['type'] == "SPEED" and item['intervalUnit'] == "SEC":
					duration = len(item['values']) * item['intervalMetric'] * 1000
					return 1
		except:
			duration = 0
	
def get_distance(workout):
	try:
		a = workout['activity']['distance']
		return 1
	except:
		return 0
		
def get_weather(workout):
	try:
		a = workout['activity']['tags']['weather']
		return 1
	except:
		return 0
		
def get_terrain(workout):
	try:
		a = workout['activity']['tags']['terrain']
		return 1
	except:
		return 0
		
def get_gps(workout):
	try:
		if workout['activity']['gps']:
			return 1
		else:
			return 0
			
	except:
		return 0
def get_fuel(workout):
	try:
		a = workout['activity']['fuel']
		if a!=0:
			return 1
		else:
			return 0
	except:
		return 0
		
def get_calories(workout):
	try:
		a = workout['activity']['calories']
		if a!=0:
			return 1
		else:
			return 0
	except:
		return 0
		
		
IN_FILE = open("crappy_workout_json.txt", "r")
for user in IN_FILE:
	try:
		data = json.loads(user)
		for workout in data['workouts']:
			num_dur += get_duration(workout)
			num_dist += get_distance(workout)
			num_weather += get_weather(workout)
			num_terrain += get_terrain(workout)
			num_gps += get_gps(workout)
			fuel += get_fuel(workout)
			calories += get_calories(workout)
	except:
		continue
print num_dur
print num_dist
print num_weather
print num_terrain
print num_gps
print fuel
print calories