import tweetstream
			
while True:
	try:
		with tweetstream.FilterStream("csce489", 'lmgtfy', track = ['nikeplus']) as stream:
			for tweet in stream:
				line = tweet['text']
				line = line.strip()
				words = line.split()
				for word in words:
					if 'http:' in word:
						try:
							with open('links.txt', 'a') as myfile:
								myfile.write(word + '\n')
						except:
							continue
				
	except:
		continue 