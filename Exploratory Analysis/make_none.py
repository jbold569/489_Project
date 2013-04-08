import json

f = open('master_tag_list.txt', 'r')
for line in f:
	data = json.loads(line)
	dict = data.fromkeys(data.keys(), None)
	print dict