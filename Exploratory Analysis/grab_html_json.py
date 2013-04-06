import urllib
import json

json_data = open("link_json.txt")
data = json.load(json_data)

def process(link):
	f = urllib.urlopen(link)
	s = f.read()
	f.close()
	print s

for item in data:
	list = data[item]
	for link in list:
		process(link)