import utils

class Athlete:
	def __init__(self, id=None, data=None):
		if id:
			self.id = id
			self.workouts = []
		if data:
			self.loadObject(data)
			
	# This function expects a dictionary of the data
	def loadObject(self, data):
		self.id = data['id']
		self.gender = utils.sGet(data, 'gender')
		for w in data['workouts']:
			workout = Workout()
			self.workouts.append(workout.loadObject(w))
			
	def addWorkout(self, workout):
		self.workouts.append(workout)
		if len(self.workouts) == 1:
			self.gender = self.workouts[0].gender
		
	
	def toDict(self):
		data = {}
		data['id'] = self.id
		data['gender'] = self.gender
		data['workouts'] = []
		for workout in self.workouts:
			data['workouts'].append(workout.toDict())
		return data

class Workout:
	def __init__(self, data = None):
		if data:
			self.loadObject(data)
		
	def loadRawData(self, activity, workout):
		self.id = utils.sGet(activity, 'activityId')
		self.distance = utils.sGet(activity, 'distance')
		self.calories = utils.sGet(activity, 'calories')
		self.fuel = utils.sGet(activity, 'fuel')
		self.gender = utils.sGet(workout, 'gender')
		
		self.get_duration(activity)
		# Minutes per mile
		try:
			self.avg_pace = self.duration/(self.distance/1.6)
		except:
			self.avg_pace = 0
		self.status = utils.sGet(activity, 'status')
		self.date = utils.sGet(activity, 'startTimeUtc')
		self.time_zone = utils.sGet(activity, 'timeZone')
		
	def loadObject(self, data):
		self.distance, self.duration, self.avg_pace, self.calories, self.fuel = data['basic']
		self.status = data['info']['status']
		self.date = data['info']['date']
		self.time_zone = data['info']['time_zone']
		self.id = data['info']['id']
		self.pace = data['advanced']['pace']
		
	def get_duration(self, workout):
		duration = 0
		self.duration = utils.sGet(workout, 'duration')/60000
		self.pace_vec = []
		try:
			for item in workout['history']:
				if item['type'] == "SPEED" and item['intervalUnit'] == "SEC":
					self.duration = len(item['values']) * item['intervalMetric'] / 60.
					self.pace_vec = item['values']
		except:
			self.duration = 0
		print "Duration: ", self.duration
	def toDict(self):
		data = {}
		data['basic'] = [self.distance, self.duration, self.avg_pace, self.calories, self.fuel]
		data['info'] = {}
		data['info']['status'] = self.status
		data['info']['date'] = self.date
		data['info']['time_zone'] = self.time_zone
		data['info']['id'] = self.id
		data['advanced'] = {}
		data['advanced']['pace'] = self.pace_vec
		
		return data