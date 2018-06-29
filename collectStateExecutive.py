import os
import csv
from datetime import datetime
from subprocess import Popen, PIPE

home = "\\\\romeo\\SPE\\2018NYSElections\\State\\executive"

currentTime = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
logFile = os.path.join(home, "executive.log")
log = open(logFile, "a")
currentTime = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
log.write("\nStarted at " + currentTime)


input = os.path.join(home, "twitterIDs.csv")

f = open(input, "r")

data = csv.reader(f, delimiter="|")

for row in data:
	office = row[0].strip()
	party = row[1].strip()
	name = row[2].strip()
	switch = row[4].strip()
	twitterName = row[3].strip()
			
	officePath = os.path.join(home, office)
	if not os.path.isdir(officePath):
		os.mkdir(officePath)
	
	partyPath = os.path.join(officePath, party + "-" + name)
	if not os.path.isdir(partyPath):
		os.mkdir(partyPath)
	
	if len(switch) > 0:
	
		currentTime = str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
		command = "twarc timeline " + twitterName + " > \"" + os.path.join(partyPath, currentTime + ".jsonl") + "\""
		print (command)
		log.write("\n	Running: " + command)
		collectTweets = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = collectTweets.communicate()
		if len(stdout) > 0:
			print(stdout)
			log.write("\n")
			log.write(stdout.decode("utf-8"))
		if len(stderr) > 0:
			print(stderr)
			log.write("\n")
			log.write(stderr.decode("utf-8"))

f.close()
log.close()