import requests, json
import time

url = "http://search.twitter.com/search.json?q=nikeplus&rpp=100&since_id=%s&include_entities=true&result_type=mixed"

previous_max_id = ""
sleep = 1

# Get where we last left off
file = open("out_tweets.txt",'r')
for line in file:
	tweet = json.loads(line)
	previous_max_id = tweet["id_str"]

# Data collection loop Sleep for a minute after 2 calls	
while True:
	r = requests.get(url%(previous_max_id))

	if r.status_code == 200:
		reply = r.json()
		previous_max_id = reply['max_id_str']
		
		file = open("out_tweets.txt", 'a')
		for tweet in reply['results']:
			file.write(json.dumps(tweet, separators=(',',':'))+'\n')
		file.close()
	else:
		print r.status_code
		
	sleep ^= 1
	if sleep: time.sleep(60)
	