import urllib
import json
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import re

regex_1 = re.compile("(?<=settings\s=\s)[\w\s\S]+(?=\swindow.np)")

class HTML_json:
	#used to keep track of all features present - to be used for cleaning later
	features_track = {}

	#pre_key_list is for nested dictionaries
	def update_features(self, json):
		self.features_track.update(json)

	def process_individual(self, data):
		dict = {'user_id' : data['user_id'], 'workouts' : []}
		for link in data['workouts']:
			dict['workouts'].append(self.grab_HTML(link))
		return dict
	
	def clean(self,js):
		return js.replace('\n', '').replace('\t', ' ').replace(';', '').replace('\'', '"')
		
	def parse_1(self,line):
		list = regex_1.findall(line)
		if len(list) > 0:
			return json.loads(list[0])
		else:
			return None
			
	def parse_simple(self,line):
		l = line.partition('=')[2].strip()
		return json.loads(l)
		
	def parse_var(self,line):
		l = line.partition('=')[2].strip()
		if "friend" in line:
			return json.loads('{"friendCount" : ' + l + '}')
		else:
			return json.loads('{"deviceType" : ' + l + '}')

	def grab_HTML(self,link):
		workout_dict = {}
		f = None
		s = None
		try:
			f = urllib.urlopen(link)
			s = f.read()
			f.close()
		except:
			return
		soup = BeautifulSoup(''.join(s))
		js= soup.findAll('script')
		for j in js:
			try:
				mystring = j.text.encode('utf-8')
				if "window.np.settings = " in mystring:
					d = self.parse_1(self.clean(mystring))
					self.update_features(d)
					workout_dict.update(d)
				if "window.np.share_data = " in mystring:
					d = self.parse_simple(self.clean(mystring))
					self.update_features(d)
					workout_dict.update(d)
				if "window.np.baked_data =" in mystring:
					d = self.parse_simple(self.clean(mystring))
					self.update_features(d)
					workout_dict.update(d)
				if "deviceType =" in mystring:
					d = self.parse_var(self.clean(mystring))
					self.update_features(d)
					workout_dict.update(d)
				if "window.np.settings.user_settings =" in mystring:
					d = self.parse_simple(self.clean(mystring))
					self.update_features(d)
					workout_dict.update(d)
				if "window.np.friendCount =" in mystring:
					d = self.parse_var(self.clean(mystring))
					self.update_features(d)
					workout_dict.update(d)
			except Exception,e: 
				print str(e) 
				continue
		return workout_dict

				
h = HTML_json()
FILE = open('crappy_workout_json.txt', 'w')
json_data = open("link_json.txt")
for line in json_data:
	data = json.loads(line)
	user = h.process_individual(data)
	json.dump(user, FILE)
	FILE.write('\n')
	
log = open('master_tag_list.txt', 'w')
json.dump(h.features_track, log)

	


