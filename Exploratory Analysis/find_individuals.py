import os
from collections import defaultdict
import json

class tweet_links:
	num_lines = 0
	num_usable = 0
	user_links = defaultdict(list)
	
	def get_useable(self):
		for item in self.user_links:
			self.num_usable += len(self.user_links[item])

	def execute(self, file_path):
		file = open(file_path, 'r')
		for line in file:
			self.num_lines += 1
			self.process(line)
		file.close()
		self.remove_none()
		self.get_useable()
		print "Number of transactions: ",  self.num_lines
		print "Number of usable lines: ", self.num_usable
		print "Number of unique users: ", len(self.user_links)
		print "==================================="
		print "Writing to link_json.txt"
		print "==================================="
		self.write_results()
	
	def write_results(self):
		with open('link_json.txt', 'w') as outfile:
			for item in self.user_links:
				dict = {'user_id' : item, 'workouts' : self.user_links[item]}
				json.dump(dict, outfile)
				outfile.write('\n')
		with open('link_json_log.txt', 'w') as outlog:
			outlog.write("Number of transactions: " + str(self.num_lines) + '\n')
			outlog.write("Number of usable lines: " + str(self.num_usable) + '\n')
			outlog.write("Number of unique users: " + str(len(self.user_links)) + '\n')
		print 'Done'
		
	def remove_none(self):
		items_to_remove = []
		for item in self.user_links:
			list = self.user_links[item]
			num_nones = 0
			for word in list:
				if word == None:
					num_nones += 1
			for i in range(0, num_nones):
				list.remove(None)
			if len(list) == 0:
				items_to_remove.append(item)
		for item in items_to_remove:
			self.user_links.pop(item)

	def grab_link(self,tweet):
		text = tweet['text']
		line = text.strip()
		words = line.split()
		for word in words:
			if 'http:' in word:
				return word
	
	def process(self,line):
		tweet = json.loads(line)
		self.user_links[tweet['from_user_id']].append(self.grab_link(tweet))
		
def main():
	print "Beginning Link Grab"
	print "==================================="
	t = tweet_links()

	BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
	FILE = os.path.join(BASE_DIR, 'out_tweets.txt')
	t.execute(FILE)
	
if __name__ == "__main__":main()