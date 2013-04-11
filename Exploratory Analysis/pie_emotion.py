import json
from collections import defaultdict
import numpy as np
from pylab import *

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
		
file = open("crappy_workout_json.txt")

gps = [0,0]
emotions = defaultdict(int)
weather = defaultdict(int)
temperatures = []
distances = []
terrain = defaultdict(int)

for line in file:
	data = sLoad(line)
	if data:
		for workout in sGet(data,'workouts'):
			activity = sGet(workout, 'activity')
			if sGet(activity,'gps'):
				gps[1] += 1
			else:
				gps[0] += 1
			tags = sGet(activity,'tags')
			
			incStat(emotions, tags, 'emotion')
			incStat(weather, tags, 'weather')
			incStat(terrain, tags, 'terrain')
			appendStat(temperatures, tags, 'temperature')
			appendStat(distances, activity, 'distance')
			
file.close()
#emotions = {u'amped': 241, u'injured': 135, u'great': 2367, u'so_so': 1617, u'tired': 547, 'NA': 3857, u'unstoppable': 2187}
figure(1, figsize=(8,8))
ax = axes([0.1, 0.1, 0.8, 0.8])
labels = emotions.keys()
total = sum(emotions.values())
fracs = [float(elem)/total*100 for elem in emotions.values()]
pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True,colors=("b","g","r","y","c", "#eeefff", "#ee0fff", "#0eefff"))
title("Athletes' Emotions out of " +str(total)+ " Workouts")

figure(2, figsize=(8,8))
ax = axes([0.1, 0.1, 0.8, 0.8])
labels = ['Disabled', 'Enabled']
total = sum(gps)
fracs = [float(elem)/total*100 for elem in gps]
pie(fracs, labels = labels,autopct='%1.1f%%', shadow=True)
title("GPS enabled out of " +str(total)+ " Workouts")

figure(3, figsize=(8,8))
ax = axes([0.1, 0.1, 0.8, 0.8])
labels = weather.keys()
total = sum(weather.values())
fracs = [float(elem)/total*100 for elem in weather.values()]
pie(fracs, labels = labels,autopct='%1.1f%%', shadow=True, colors=("b","g","r","y","c", "#eeefff", "#ee0fff", "#0eefff"))
title("Weather out of " +str(total)+ " Workouts")

figure(4, figsize=(8,8))
ax = axes([0.1, 0.1, 0.8, 0.8])
labels = terrain.keys()
total = sum(terrain.values())
fracs = [float(elem)/total*100 for elem in terrain.values()]
pie(fracs, labels = labels,autopct='%1.1f%%', shadow=True, colors=("b","g","r","y","c", "#eeefff", "#ee0fff", "#0eefff"))
title("Terrain out of " +str(total)+ " Workouts")

temperatures = [1.8*(float(t.replace('C', ''))+32) for t in temperatures if t != '0']
distances = [d*0.621371192 for d in distances]
buckets = range(20, 150, 5)

figure(5)
hist(temperatures, bins=buckets)
title("Temperature Ranges out of " +str(total)+ " Workouts")

show()