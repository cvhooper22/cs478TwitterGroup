#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contain the user credentials to access Twitter API 
access_token = "ENTER TOKEN HERE"
access_token_secret = "ENTER TOKEN HERE"
consumer_key = "ENTER TOKEN HERE"
consumer_secret = "ENTER TOKEN HERE"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
	filenum = 1
	tweetcount = 0
	
	def on_data(self, data):
		if self.tweetcount >= 500:
			self.filenum += 1
			self.tweetcount = 0
		filename = ("data/twdata" + str(self.filenum) + ".txt")
		with open(filename, "a") as f:
			f.write(data)
			f.write(";\n")
		self.tweetcount += 1
		return True
	
	def on_error(self, status):
		print status


if __name__ == '__main__':
	
	keywordsArray = []
	keywordsPath = "keywords.txt"
	with open(keywordsPath, "r") as f:
		for keywordLine in f:
			keywordsArray.append(keywordLine.strip())
	
	print keywordsArray
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	
	#This line filter Twitter Streams to capture data by certain keywords
	stream.filter(track=keywordsArray)