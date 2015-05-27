import os
import json
import pandas as pd
import matplotlib.pyplot as plt



input_data_path = 'data\\'
output_data_path = 'endata\\'

filenames = os.listdir("data")

for filename in filenames:
	tweets_data = []
	input_path = input_data_path + filename
	print input_path
	tweets_file = open(input_path, "r")
	for line in tweets_file:
		try:
			tweet = json.loads(line)
			tweets_data.append(tweet)
		except:
			continue

	print len(tweets_data)

	#tweets = pd.DataFrame()

	#tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
	#tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
	#tweets['country'] = map(lambda tweet: tweet['place'][country] if tweet['place'] != None else None, tweets_data)

	for tweet in tweets_data:
		if 'lang' in tweet:
			if tweet['lang'] == "en":
				output_path = output_data_path + filename
				with open(output_path, "a") as f:
					f.write(json.dumps(tweet).encode('utf8'))
					f.write('\n\n')

print "Done"