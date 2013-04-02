import os, gzip, cjson
from library.twitter import TweetFiles
from library.file_io import FileIO
from library.geo import isWithinBoundingBox, getCenterOfMass,\
    getHaversineDistance
from settings import us_boundary

year = 2012
OutputDir = '/mnt/chevron/bde/Data/NikePlus/SampleRuns/%d/%d'
bdeDataDir = '/mnt/chevron/bde/Data/TweetData/SampleTweets/%d/%d/%d'
#checkinsFile = '/mnt/chevron/dataset/twitter/reduced_geo/%s'%year+'_%s'

def tweetFilesIterator():
	global year
	for month in range(1, 12):
		outputFile = OutputDir%(year,month)
		for day in range(1, 32):
			tweetsDayFolder = bdeDataDir%(year,month, day)
			if os.path.exists(tweetsDayFolder):
				for _, _, files in os.walk(tweetsDayFolder):
					for file in files: yield outputFile, tweetsDayFolder+file

def isNikePlus(data):
	return 'nikeplus' in data['entities']['hashtags']

for outputFile, file in tweetFilesIterator():
	print 'Parsing: %s'%file
	for line in gzip.open(file, 'rb'):
		try:
			data = cjson.decode(line)
			if isNikePlus(data):
				FileIO.writeToFileAsJson(data, outputFile)
		except Exception as e: 
			#print line
			print e