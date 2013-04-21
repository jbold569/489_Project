import utils
import json 
from DataObjects import *
import numpy as np

file = open("crappy_workout_json.txt", "r")
out = open("clean_data.txt", 'w')

athletes = []

i = 0
for line in file:
	i += 1
	data = utils.sLoad(line)
	user = Athlete(utils.sGet(data, 'user_id'))
	invalidUser = False
	workouts = utils.sGet(data, 'workouts')
	if not workouts: 
		continue
	for w in workouts:
		activity = utils.sGet(w, 'activity')
		if not activity:
			print "Missing activity information, skipping..."
			invalidUser = True
			break
		workout = Workout()
		workout.loadRawData(activity, w)
		#print "Workout: %s, distance: %f"%(workout.id, workout.distance)
		user.addWorkout(workout)
		
	if invalidUser:
		continue
		
	athletes.append(user)
	#print "User's gender: ", user.gender
	out.write(json.dumps(user.toDict())+'\n')

file.close()
out.close()