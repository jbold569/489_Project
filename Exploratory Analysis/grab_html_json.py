import urllib
import json
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

class HTML_json:
	features_count = defaultdict(int)
	
def grab_HTML(link):
	f = urllib.urlopen(link)
	s = f.read()
	f.close()
	soup = BeautifulSoup(''.join(s))
	js= soup.findAll('script')
	for j in js:
		try:
			mystring = j.text.encode('ascii')
			print mystring + '\n\n'
		except:
			continue

json_data = open("link_json.txt")
for line in json_data:
	data = json.loads(line)
	for link in data['workouts']:
		grab_HTML(link)

