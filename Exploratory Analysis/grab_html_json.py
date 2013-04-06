import urllib
import json
from collections import defaultdict

class HTML_json:
	features_count = defaultdict(int)
	
def grab_HTML(link):
	f = urllib.urlopen(link)
	s = f.read()
	f.close()
	print s

json_data = open("link_json.txt")
for line in json_data:
	data = json.loads(line)
	for link in data['workouts']:
		grab_HTML(link)

