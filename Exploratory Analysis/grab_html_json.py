import urllib
import json
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import re

regex_1 = re.compile("(?<=settings\s=\s)[\w\s\S]+(?=\swindow.np)")

class HTML_json:
	features_count = defaultdict(int)
	
def clean(js):
	return js.replace('\n', '').replace('\t', ' ').replace(';', '').replace('\'', '"')
def parse_1(line):
	list = regex_1.findall(line)
	if len(list) > 0:
		return json.loads(list[0])
	else:
		return None
		
def parse_simple(line):
	l = line.partition('=')[2].strip()
	return json.loads(l)
	
def parse_var(line):
	l = line.partition('=')[2].strip()
	if "friend" in line:
		return json.loads('{"friendCount" : ' + l + '}')
	else:
		return json.loads('{"deviceType" : ' + l + '}')

def grab_HTML(link):
	f = urllib.urlopen(link)
	s = f.read()
	f.close()
	soup = BeautifulSoup(''.join(s))
	js= soup.findAll('script')
	for j in js:
		try:
			mystring = j.text.encode('utf-8')
			if "window.np.settings = " in mystring:
				print parse_1(clean(mystring))
			if "window.np.share_data = " in mystring:
				print parse_simple(clean(mystring))
			if "window.np.baked_data =" in mystring:
				print parse_simple(clean(mystring))
			if "deviceType =" in mystring:
				print parse_var(clean(mystring))
			if "window.np.settings.user_settings =" in mystring:
				print parse_simple(clean(mystring))
		 	if "window.np.friendCount =" in mystring:
				print parse_var(clean(mystring))
		except Exception,e: 
			print str(e) 
			continue

json_data = open("link_json.txt")
for line in json_data:
	data = json.loads(line)
	for link in data['workouts']:
		grab_HTML(link)

