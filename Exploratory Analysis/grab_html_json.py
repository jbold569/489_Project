import urllib
import json
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

class HTML_json:
	features_count = defaultdict(int)
	
def clean(js):
	print js.replace('\n', '').replace('\t', ' ').replace(';', '')
	
def grab_HTML(link):
	f = urllib.urlopen(link)
	s = f.read()
	f.close()
	soup = BeautifulSoup(''.join(s))
	js= soup.findAll('script')
	found_crit = False
	for j in js:
		try:
			mystring = j.text.encode('ascii')
			if "window.np.settings = " in mystring:
				print "found 1 \n"
				clean(mystring)
			if "window.np.share_data = " in mystring:
				print "found 2 \n"
				clean(mystring)
			if "window.np.baked_data =" in mystring:
				print "found 3 \n"
				found_crit = True
				clean(mystring)
			if "deviceType =" in mystring:
				print "found 4 \n"
				clean(mystring)
			if "window.np.settings.user_settings =" in mystring:
				print "found 5 \n"
				clean(mystring)
		 	if "window.np.friendCount =" in mystring:
				print "found 6 \n"
				clean(mystring)
			#print mystring + '\n\n'
		except:
			continue
	print found_crit, link
	print '\n\n\n\n'

json_data = open("link_json.txt")
for line in json_data:
	data = json.loads(line)
	for link in data['workouts']:
		grab_HTML(link)

