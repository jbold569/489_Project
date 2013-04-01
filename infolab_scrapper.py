import gzip
import os

path = os.getcwd()

for dirname, dirnames, filenames in os.walk(path):
	# print path to all filenames.
	for filename in filenames:
		cur = os.path.join(dirname, filename)
		try:
			with open('info_lab_links.txt', 'a') as myfile:
				for line in gzip.open(cur, 'rb'):
					myfile.write(line + '\n')
				myfile.close()
		except:
			line = "Error reading: " + cur
			with open('error_log.txt', 'a') as errorfile:
				errorfile.write(line + '\n')
			errorfile.close()
			continue
			